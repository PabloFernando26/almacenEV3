from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #panel de administración de Django
    path('admin/', admin.site.urls),
    
    # URLs de la aplicación 'productos'
    path('', include('productos.urls')),  # Rutas de la app `productos`
]

# Configuración para servir archivos de medios en desarrollo (como imágenes subidas por el usuario)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
