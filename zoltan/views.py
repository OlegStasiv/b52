from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, render_to_response
# Create your views here.
from b52 import settings
from zoltan.forms import SignUpForm
from zoltan.models import User


def groups(request):
    if request.user.is_authenticated():
        pass
        return render(request, 'hr.html')
    return redirect('/login')


def log_in(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'sign_in':
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin')
                return redirect('/')
            return redirect('/login')
        elif request.POST.get('submit') == 'sign_up':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('/')
    return render_to_response('login.html')


def log_out(request):
    logout(request)
    return redirect('/login')