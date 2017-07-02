from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'sample_path', views.sample_path, name='sample_path'),
    url(r'average', views.average, name='average'),
    url(r'error', views.error, name='error'),
]
