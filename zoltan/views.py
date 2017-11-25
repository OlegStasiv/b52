import warnings
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import deprecate_current_app
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect, render_to_response, resolve_url
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.deprecation import RemovedInDjango21Warning
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from zoltan.forms import SignUpForm, PasswordResetForm
from zoltan.models import Task, TaskCandidates

UserModel = get_user_model()


def index(request):
    if request.user.is_authenticated():
        return redirect('tasks')
    return render_to_response('index.html')


def log_in(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'Sign In':
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin')
                return redirect('/tasks')
            return redirect('/login')
        elif request.POST.get('submit') == 'Sign Up':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('/tasks')
    return render_to_response('login.html')


def log_out(request):
    logout(request)
    return redirect('/login')


def password_reset(request,
                   template_name='login',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   extra_context=None,
                   html_email_template_name=None,
                   extra_email_context=None):
    warnings.warn("The password_reset() view is superseded by the "
                  "class-based PasswordResetView().",
                  RemovedInDjango21Warning, stacklevel=2)
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
                'extra_email_context': extra_email_context,
            }
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
            # messages.success(request, 'Form submission successful')
            # return render(request, 'login.html')

    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
@deprecate_current_app
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    warnings.warn("The password_reset_confirm() view is superseded by the "
                  "class-based PasswordResetConfirmView().",
                  RemovedInDjango21Warning, stacklevel=2)
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('/login')
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


def tasks(request):
    if request.user.is_authenticated():
        tasks = Task.objects.filter(user_id=request.user.id)
        context = {'tasks': tasks}
        return render(request, 'tasks.html', context)
    return redirect('/tasks')


def detail_tasks(request, id):
    if request.user.is_authenticated():
        if request.is_ajax():
            obj = Task.objects.get(id=id)
            data = {"task_name": obj.task_name, "linkedin_url":obj.linkedin_url,
                    "connect_message_text": obj.connect_message_text, "forward_message": obj.forward_message_text,
                    "connection_percent": obj.connection_percent, "brake_every": obj.brake_every,
                    "brake_on": obj.brake_for, "connect_with_message": obj.connect_with_message}
            return JsonResponse({'data': data})
        else:
            raise Http404


def candidates(request):
    if request.user.is_authenticated():
        task_id = request.GET.get('task_id')
        tasks = Task.objects.filter(user_id=request.user.id)
        candidates = TaskCandidates.objects.filter(task__id=task_id)
        context = {'candidates': candidates, 'tasks': tasks}
        return render(request, 'candidates.html', context)
    return redirect('/login')