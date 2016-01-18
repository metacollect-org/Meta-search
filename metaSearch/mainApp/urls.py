from django.conf.urls import url

from . import views
from . import views_api

app_name = 't'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<project_id>\d+)/$', views.detail, name='detail'),
    url(r'^search/', views.search_titles, name='title'),
    url(r'^new/', views.ProjectNewView.as_view(), name='new'),
]
