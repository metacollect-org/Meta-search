from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views
from . import views_api

app_name = 't'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    # url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/mainApp/'}, name='logout'),
    # url(r'^register/$', views.register, name='register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^(?P<project_id>\d+)/$', views.detail, name='detail'),
    url(r'^search/autocomplete', views.search_titles, name='title'),
    url(r'^search/fulltext', views.search_fulltext, name='fulltext'),
    # url(r'^new/', views.ProjectNewView.as_view(), name='new'),
    url(r'^new/', views.join_page, name='new'),
    url(r'^(?P<project_id>\d+)/edit/$', views.edit_page, name='project-edit'),
    url(r'^(?P<project_id>\d+)/delete/$', views.delete_page, name='project-delete'),
    url(r'^data/', views.data, name='data'),
    url(r'^accounts/profile', views.user_profile, name='user_profile'),
    url(r'^accounts/projects', views.user_projects, name='user_projects'),
]
