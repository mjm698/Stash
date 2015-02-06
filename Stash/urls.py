from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Stash.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'polymer.views.home', name='home'),
    url(r'^stash/$', 'polymer.views.stash', name='stash'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
