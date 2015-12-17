from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<project_id>\d+)/$', views.detail, name='detail'),
    url(r'^search/', views.search_titles, name='title'),

]
