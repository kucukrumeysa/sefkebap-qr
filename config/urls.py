from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from decouple import config

# Dynamic Admin Path
ADMIN_URL = config('ADMIN_URL', default='admin/')
if ADMIN_URL and not ADMIN_URL.endswith('/'):
    ADMIN_URL += '/'

admin.site.site_header = 'Şef Kebab Yönetim Paneli'
admin.site.site_title = 'Şef Kebab Admin'
admin.site.index_title = 'Menü Yönetimi'

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path('', include('apps.menu.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
