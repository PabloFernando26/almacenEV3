from django import forms
from .models import Producto
from django.contrib.auth.forms import AuthenticationForm

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'cantidad', 'imagen']

    # Validación 'precio'
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor que cero.')
        return precio

    # Validación 'cantidad'
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad < 0:
            raise forms.ValidationError('La cantidad no puede ser negativa.')
        return cantidad

    # Validación del nombre del producto
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre:
            raise forms.ValidationError('El nombre del producto es obligatorio.')
        return nombre

    # Validación de la imagen (si se proporciona)
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            # Verificar si el archivo de imagen tiene el formato correcto (opcional)
            if not imagen.name.endswith(('jpg', 'jpeg', 'png')):
                raise forms.ValidationError('La imagen debe ser en formato JPG, JPEG o PNG.')
        return imagen


# Formulario de Login
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, label='Correo electrónico')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
