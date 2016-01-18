from django.conf.urls import url, include
from rest_framework import routers
from mainApp import views_api

# router = routers.DefaultRouter()
# router.register(r'projects', views_api.ProjectViewSet)
# router.register(r'categories', views_api.CategoryViewSet)
# router.register(r'langs', views_api.PageLanguageViewSet)
# router.register(r'kinds', views_api.KindViewSet)
# router.register(r'programminglanguage', views_api.ProgrammingLanguageViewSet)



app_name = 'mainApp'
urlpatterns = [
    url(r'^allprojects/', views_api.project_list),
    url(r'^project/(?P<pk>[0-9]+)$', views_api.project_detail),
    url(r'^projectsearch/(?P<text>[0-9,a-z,A-Z]+)$', views_api.project_search_fulltext),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
