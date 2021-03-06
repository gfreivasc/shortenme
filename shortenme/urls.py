"""shortenme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib.auth.views import login, logout
import shorten.views

urlpatterns = [
    url(r'^$', shorten.views.IndexView.as_view(), name='index'),
    url(r'^(?P<hash>\w+)$', shorten.views.LinkRedirectView.as_view(), name='redirect'),
    url(r'^l/$', shorten.views.LinkCreate.as_view(), name='link-create'),
    url(r'^l/(?P<pk>[0-9]+)/$', shorten.views.LinkDetails.as_view(), name='link-details'),
    url(r'^links/', shorten.views.UserLinks.as_view(), name='user-links'),
    # url(r'^db', shorten.views.db, name='db'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login, kwargs={'template_name': 'shorten/login.html'}, name='login'),
    url(r'^logout/$', logout, kwargs={'template_name': 'shorten/logged_out.html'}, name='logout'),
    url(r'^new_user/$', shorten.views.UserCreate.as_view(), name='new-user'),
]
