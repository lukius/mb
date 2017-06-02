from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'plot', views.plot, name='plot'),
]
