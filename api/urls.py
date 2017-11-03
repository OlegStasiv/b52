from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.UserViewSet.as_view()),
    url(r'^tasks/$', views.TaskViewSet.as_view()),
    url(r'^tasks/(?P<pk>[0-9]+)$', views.TaskDetailViewSet.as_view()),
    url(r'^candidate/$', views.TaskCandidateViewSet.as_view()),
]
