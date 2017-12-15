"""b52 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from api.views import obtain_auth_token
from zoltan import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.log_in, name='login'),
    url(r'^logout/', views.log_out, name='logout'),
    url(r'^api/', include('api.urls')),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^profile/$', views.change_profile, name='change_profile'),
    url(r'^tasks/(?P<id>\d+)', views.detail_tasks, name='detail_tasks'),
    url(r'^tasks/', views.tasks, name='tasks'),
    url(r'^candidates/(?P<id>\d+)', views.candidates, name='candidates'),
    url(r'^candidates/', views.candidates, name='candidates'),
    url(r'^points/', views.points, name='points'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),

]
