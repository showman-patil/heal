from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.views import serve as static_serve
from django.views.static import serve as media_serve
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Always expose static files when running via Django app server.
# This keeps admin CSS/JS working even if DEBUG is off in local env.
urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', static_serve, {'insecure': True}),
    re_path(r'^media/(?P<path>.*)$', media_serve, {'document_root': settings.MEDIA_ROOT}),
]

admin.site.site_header = 'Heal-Delight Admin'
admin.site.site_title = 'Heal-Delight'
admin.site.index_title = 'Welcome to Admin'
