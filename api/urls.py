from django.conf.urls import url

from api.views import check_version
from . import views

urlpatterns = [
    url(r'^users/$', views.UserViewSet.as_view()),
    url(r'^tasks/$', views.TaskViewSet.as_view()),
    url(r'^tasks/(?P<pk>[0-9]+)$', views.TaskDetailViewSet.as_view()),
    url(r'^tasks/(?P<pk>[0-9]+)/candidates/$', views.TaskDetailCandidate.as_view()),
    url(r'^candidate/$', views.TaskCandidateViewSet.as_view()),
    url(r'^candidate/(?P<pk>[0-9]+)$', views.CandidateProfile.as_view()),
    url(r'^check_version$', check_version, name='check_version')
]
