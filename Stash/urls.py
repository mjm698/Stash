from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'polymer.views.home', name='home'),

    url(r'^view/$', 'polymer.views.view', name='view'),
    url(r'^viewContent/$', 'polymer.views.viewContent', name='viewContent'),

    url(r'^login/$', 'login.views.login_user', name='login'),
    url(r'^logout/$', 'login.views.logout_user', name='logout'),
    url(r'^register/$', 'login.views.register', name='register'),

    url(r'^comment/$', 'polymer.views.comment', name='comment'),
    url(r'^content/$', 'polymer.views.content', name='content'),
    url(r'^parse/$', 'polymer.views.parse', name='parse'),
    url(r'^stash/$', 'polymer.views.stash', name='stash'),
    url(r'^stash/name/$', 'polymer.views.stashName', name='stashName'),
    url(r'^update/$', 'polymer.views.update', name='update'),
    url(r'^user/$', 'polymer.views.user', name='user'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
