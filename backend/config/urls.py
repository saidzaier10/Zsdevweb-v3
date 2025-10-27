from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/quotes/', include('quotes.urls')),
    path('api/portfolio/', include('portfolio.urls')),
    path('api/auth/', include('users.urls')),
]

# Pour servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)