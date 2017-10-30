from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.UserViewSet.as_view()),
    url(r'^tasks/$', views.TaskViewSet.as_view()),
    url(r'^tasks/(?P<pk>[0-9]+)$', views.TaskDetailViewSet.as_view()),
    # url(r'^candidates/$', views.CandidateViewSet.as_view()),
    # url(r'^persons/update-partial/(?P<pk>\d+)/$', UserPartialUpdateView.as_view()),

]