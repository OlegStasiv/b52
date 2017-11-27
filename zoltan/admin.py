from django.contrib import admin

# Register your models here.
from zoltan import models
from zoltan.models import Task, User, Candidate, TaskCandidates


class TaskList(admin.ModelAdmin):
    model = Task
    list_display = ("task_name", "created_at", "get_name")

    def get_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    get_name.admin_order_field = 'user'  # Allows column order sorting
    get_name.short_description = 'Task by'  # Renames column head


class UserList(admin.ModelAdmin):
    model = User

    list_display = ("get_full_name", "email", "points")

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.admin_order_field = 'id'  # Allows column order sorting
    get_full_name.short_description = 'Full name'  # Renames column head


class CandidateList(admin.ModelAdmin):
    model = Candidate
    list_display = ("full_name", "linkedin_url")



class TaskCandidateList(admin.ModelAdmin):
    model = TaskCandidates
    list_display = ("task_name", "candidate_name", "send_connect", "accept_connect", "send_message", "send_forward")

    def task_name(self, obj):
        return obj.get_task_name()

    def candidate_name(self, obj):
        return obj.get_candidate_name()


admin.site.register(models.TaskCandidates, TaskCandidateList)
admin.site.register(models.User, UserList)
admin.site.register(models.Task, TaskList)
admin.site.register(models.Candidate, CandidateList)
