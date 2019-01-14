"""resumebuilder URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from ..resume import views as resume_views
from ..user import views as user_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url('^login/$', auth_views.LoginView.as_view(), name='login'),
    url('^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^$', RedirectView.as_view(pattern_name='resumes')),

    url(r'^resumes/$', resume_views.resumes_view, name='resumes'),

    url(r'^resume/(?P<resume_id>\d+)/$', resume_views.resume_view, name='resume'),
    url(r'^resume/edit/(?P<resume_id>\d+)/$', resume_views.resume_edit_view, name='resume-edit'),
    url(r'^resume/create/$', resume_views.resume_create_view, name='resume-create'),

    url(r'^resume/(?P<resume_id>\d+)/item/edit/(?P<resume_item_id>\d+)/$', resume_views.resume_item_edit_view,
        name='resume-item-edit'),
    url(r'^resume/(?P<resume_id>\d+)/item/create/$', resume_views.resume_item_create_view,
        name='resume-item-create'),

    url(r'^user/$', user_views.account_edit_view, name='account-edit'),
    url(r'^create-account/$', user_views.account_create_view,
        name='account-create'),
]
