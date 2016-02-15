from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from mainApp import views_api

app_name = 'mainApp'
urlpatterns = [
    url(r'^projectsearch/(?P<text>[0-9,a-z,A-Z]+)$', views_api.project_search_fulltext),
    url(r'^geosearch/$', views_api.search_radius),
    url(r'^search/project$', views_api.search_project),
    url(r'^search/category$', views_api.search_category),
    url(r'^search/kind$', views_api.search_kind),
    url(r'^search/language$', views_api.search_language),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlPatterns = format_suffix_patterns(urlpatterns)