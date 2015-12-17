from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'metaSearch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^mainApp/', include('mainApp.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
