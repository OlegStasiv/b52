from __future__ import unicode_literals
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

from b52 import settings


class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password):
        """Creates and saves a User with the given email, date of
        birth and password.
        """
        if not first_name:
            raise ValueError('Users must have an first name')
        if not last_name:
            raise ValueError('Users must have an last name')
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have an password')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            password=password,
        )

        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        """Creates and saves a superuser with the given email, date of
        birth and password.
        """
        if not first_name:
            raise ValueError('Users must have an first name')
        if not last_name:
            raise ValueError('Users must have an last name')
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have an password')

        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('name'), max_length=30)
    last_name = models.CharField(_('surname'), max_length=30)
    email = models.EmailField(_('email'), unique=True)
    date_joined = models.DateTimeField(_('registered'), auto_now_add=True)
    is_active = models.BooleanField(_('is_active'), default=True)
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


class Candidate(models.Model):
    certifications = models.TextField(null=True)
    companies = models.TextField(null=True)
    educations = models.TextField(null=True)
    linkedin_url = models.TextField(null=False, unique=True)
    full_name = models.TextField(null=False)
    avatar = models.TextField(null=True)
    awards = models.TextField(null=True)
    country = models.TextField(null=True)
    courses = models.TextField(null=True)
    email = models.TextField(null=True)
    languages = models.TextField(null=True)
    projects = models.TextField(null=True)
    skills = models.TextField(null=True)
    summary = models.TextField(null=True)
    title = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.full_name


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=128, null=False, blank=False)
    linkedin_url = models.CharField(max_length=256, null=False, blank=False)
    linkedin_email = models.CharField(max_length=128, null=False, blank=False)
    linkedin_password = models.CharField(max_length=128)
    connection_percent = models.IntegerField(default=100)
    connect_note_text = models.TextField(max_length=300, null=True)
    connect_message_text = models.TextField(max_length=5000, null=True)
    forward_message_text = models.TextField(max_length=5000, null=True)
    brake_every = models.IntegerField(default=0)
    brake_for = models.IntegerField(default=0)
    connect_with_message = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    candidates = models.ManyToManyField(Candidate, through='TaskCandidates')


class TaskCandidates(models.Model):
    task = models.ForeignKey(Task)
    candidate = models.ForeignKey(Candidate)
    send_connect = models.BooleanField(default=False)
    accept_connect = models.BooleanField(default=False)
    send_message = models.BooleanField(default=False)
    send_forward = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
