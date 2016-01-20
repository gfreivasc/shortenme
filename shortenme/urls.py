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

import shorten.views

urlpatterns = [
    url(r'^$', shorten.views.IndexView.as_view(), name='index'),
    url(r'^(?P<hash>\w+)$', shorten.views.LinkRedirectView.as_view(), name='redirect'),
    url(r'^l/$', shorten.views.LinkCreate.as_view(), name='link-create'),
    url(r'^l/(?P<pk>[0-9]+)/$', shorten.views.LinkDetails.as_view(), name='link-details'),
    # url(r'^l/(?P<hash>\w+)$', shorten.LinkView.as_view(), name ='link'),
    url(r'^admin/', admin.site.urls),
]
