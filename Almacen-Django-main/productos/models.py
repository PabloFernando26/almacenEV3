from django.db import models
from django.contrib.auth.models import User

# Creación de los modelos 
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)  # Imagen de la categoría

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Imagen del producto

    def __str__(self):
        return self.nombre


# Modelo para registrar una venta
class Venta(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    productos = models.ManyToManyField(Producto, through='DetalleVenta')

    def __str__(self):
        return f"Venta {self.id} - {self.cliente.username}"


# Modelo para los detalles de la venta
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id} - {self.producto.nombre}"

    # Método para calcular el subtotal de este detalle
    def subtotal(self):
        return self.cantidad * self.precio_unitario
