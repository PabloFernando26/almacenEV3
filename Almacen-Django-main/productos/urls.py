from django.urls import path
from . import views

urlpatterns = [
    # Ruta de inicio
    path('', views.home, name='home'),  
    
    # Rutas para gestionar categorías y productos
    path('categoria/<int:categoria_id>/', views.lista_productos, name='lista_productos'), 
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),  

    # Rutas para agregar, editar y eliminar productos 
    path('categoria/<int:categoria_id>/producto/agregar/', views.agregar_producto, name='agregar_producto'),  
    path('producto/<int:producto_id>/editar/', views.editar_producto, name='editar_producto'),  
    path('producto/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),  

    # Rutas para agregar productos al carrito y ver el carrito
    path('producto/<int:producto_id>/agregar_al_carrito/', views.agregar_carrito, name='agregar_carrito'), 
    path('carrito/', views.carrito, name='carrito'),  

    # Rutas para la compra de productos
    path('compra/<int:producto_id>/', views.compra_producto, name='compra_producto'), 
    path('finalizar_compra/<int:producto_id>/', views.finalizar_compra, name='finalizar_compra'),  

    # Ruta para la compra exitosa
    path('compra_exitosa/<int:producto_id>/', views.compra_exitosa, name='compra_exitosa'),  

    # Rutas de autenticación listas recordatorio no cambiar 
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),  
    path('register/', views.register, name='register'),  
]
