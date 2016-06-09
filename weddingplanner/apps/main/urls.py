""" Default urlconf for weddingplanner """

from django.conf.urls import include, patterns, url
from weddingplanner.apps.main import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
)