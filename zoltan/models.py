from __future__ import unicode_literals
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext_lazy as _

from b52 import settings


class MyUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('Users must have an password')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('name'), max_length=30)
    last_name = models.CharField(_('surname'), max_length=30)
    email = models.EmailField(_('email'), unique=True)
    date_joined = models.DateTimeField(_('registered'), auto_now_add=True)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    points = models.IntegerField(default=1000)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return user's full name."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return user's short name."""
        return self.first_name

    def send_email_to_user(self, subject, message, from_email=None, **kwargs):
        """Send email to user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def update_points(self):
        """Minus points for user"""
        self.points = self.points - 1
        if self.points == 0:
            from zoltan.utils import send_notification_to_user
            send_notification_to_user(self, 'You rich limit of your points. Now you have 0 points')
        self.save()
        # Send new points value by socket
        from zoltan.utils import send_points_count_to_user
        send_points_count_to_user(self, self.points)


class Candidate(models.Model):
    certifications = models.TextField(null=True, blank=True)
    companies = models.TextField(null=True, blank=True)
    educations = models.TextField(null=True, blank=True)
    linkedin_url = models.TextField(null=False, blank=True)
    full_name = models.TextField(null=False)
    avatar = models.TextField(null=True, blank=True)
    awards = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    courses = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    languages = models.TextField(null=True, blank=True)
    projects = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.full_name


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    task_type = models.CharField(max_length=32, default='full')
    task_name = models.CharField(max_length=128, null=False, blank=False)
    linkedin_url = models.CharField(max_length=256, null=False, blank=False)
    linkedin_email = models.CharField(max_length=128, null=False, blank=False)
    linkedin_password = models.CharField(max_length=128)
    connection_percent = models.IntegerField(default=100)
    connect_note_text = models.TextField(max_length=300, null=True)
    connect_message_text = models.TextField(max_length=5000, null=True)
    forward_message_text = models.TextField(max_length=5000, null=True)
    brake_every = models.IntegerField(null=True)
    brake_for = models.IntegerField(null=True)
    max_send_connect = models.IntegerField(null=True)
    connect_with_message = models.BooleanField(default=False)
    continue_from_page = models.IntegerField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    candidates = models.ManyToManyField(Candidate, through='TaskCandidates')
    created_at = models.DateTimeField(auto_now_add=True)


class TaskCandidates(models.Model):
    task = models.ForeignKey(Task)
    candidate = models.ForeignKey(Candidate)
    send_connect = models.BooleanField(default=False)
    send_connect_date = models.DateTimeField(null=True)
    accept_connect = models.BooleanField(default=False)
    accept_connect_date = models.DateTimeField(null=True)
    send_message = models.BooleanField(default=False)
    send_message_date = models.DateTimeField(null=True)
    send_forward = models.BooleanField(default=False)
    send_forward_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'candidate')

    def get_task_name(self):
        """Return task's name."""
        task_name = '%s' % (self.task.task_name)
        return task_name.strip()

    def get_candidate_name(self):
        """Return candidate's name."""
        candidate_name = '%s' % (self.candidate.full_name)
        return candidate_name.strip()


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications')
    text = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(pre_save, sender=TaskCandidates)
def set_active_from_on_update(sender, instance, **kwargs):
    if instance.send_connect is True and instance.send_connect_date is None:
        instance.send_connect_date = datetime.now()
    if instance.accept_connect is True and instance.accept_connect_date is None:
        instance.accept_connect_date = datetime.now()
    if instance.send_message is True and instance.send_message_date is None:
        instance.send_message_date = datetime.now()
    if instance.send_forward is True and instance.send_forward_date is None:
        instance.send_forward_date = datetime.now()


class Build(models.Model):
    WINDOWS = 1
    MAC = 2
    LINUX = 3
    OTHER = 4

    STATUS_CHOICES = (
        (WINDOWS, 'WINDOWS'),
        (MAC, 'MAC'),
        (LINUX, 'LINUX'),
        (OTHER, 'OTHER'),
    )

    system = models.IntegerField(choices=STATUS_CHOICES, default=WINDOWS)
    description = models.CharField(max_length=255, blank=True)
    version = models.CharField(max_length=128, blank=False)
    file = models.FileField(upload_to='builds/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
