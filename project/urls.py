from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import index, health
from keyword_engine.views import index as index_custom
from keyword_engine.views import extract_keywords

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index),
    url(r'^health$', health),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^custom$', index_custom),
    url(r'^extract-keywords', extract_keywords),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
