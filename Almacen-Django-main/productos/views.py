from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Categoria, Producto
from .forms import ProductoForm

# Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente.')
            return redirect('home')
        else:
            messages.error(request, 'Credenciales incorrectas. Intenta de nuevo.')
    else:
        form = AuthenticationForm()

    return render(request, 'productos/login.html', {'form': form})

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('home')

# Vista para registrar un nuevo usuario
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Hubo un error al crear la cuenta. Intenta nuevamente.')
    else:
        form = UserCreationForm()

    return render(request, 'productos/register.html', {'form': form})

# Vista para mostrar todas las categorías
def home(request):
    categorias = Categoria.objects.all()
    return render(request, 'productos/home.html', {'categorias': categorias})

# Lista de los productos de una categoría específica
def lista_productos(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'productos/lista_productos.html', {'categoria': categoria, 'productos': productos})

# Muestra los detalles de un producto específico
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    categoria = producto.categoria
    return render(request, 'productos/detalle_producto.html', {'producto': producto, 'categoria': categoria})

# Agregar un nuevo producto a una categoría (solo para administradores)
@login_required
def agregar_producto(request, categoria_id):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para agregar productos.')
        return redirect('home')

    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.categoria = categoria
            producto.save()
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect('lista_productos', categoria_id=categoria.id)
        else:
            messages.error(request, 'Hubo un error al agregar el producto. Por favor, revisa los campos.')
    else:
        form = ProductoForm()

    return render(request, 'productos/agregar_producto.html', {'form': form, 'categoria': categoria})

# Vista para editar un producto
@login_required
def editar_producto(request, producto_id):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para editar productos.')
        return redirect('home')

    producto = get_object_or_404(Producto, id=producto_id)
    categoria = producto.categoria

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('lista_productos', categoria_id=categoria.id)
        else:
            messages.error(request, 'Hubo un error al actualizar el producto. Por favor, revisa los campos.')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto, 'categoria': categoria})

# Vista para eliminar un producto
@login_required
def eliminar_producto(request, producto_id):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para eliminar productos.')
        return redirect('home')

    producto = get_object_or_404(Producto, id=producto_id)
    categoria = producto.categoria

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('lista_productos', categoria_id=categoria.id)
    else:
        return render(request, 'productos/eliminar_producto.html', {'producto': producto, 'categoria': categoria})
    
# Vista para agregar un producto al carrito
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Aquí puedes agregar la lógica para manejar el carrito de compras
    carrito = request.session.get('carrito', [])
    carrito.append(producto.id)  # Agrega el producto al carrito
    request.session['carrito'] = carrito  # Guarda el carrito actualizado en la sesión

    messages.success(request, f'Producto {producto.nombre} agregado al carrito.')
    return redirect('detalle_producto', producto_id=producto.id)

# Vista para ver el carrito
def carrito(request):
    # Obtener los productos del carrito desde la sesión
    carrito_items = request.session.get('carrito', [])
    
    # Si el carrito está vacío, agregar un mensaje
    if not carrito_items:
        messages.info(request, 'Tu carrito está vacío.')

    # Obtener los detalles de los productos en el carrito
    productos_carrito = Producto.objects.filter(id__in=carrito_items)

    # Mostrar la información del carrito en el template
    return render(request, 'productos/carrito.html', {'carrito_items': productos_carrito})

# Vista para ver los detalles de un producto y continuar con la compra
def compra_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'productos/compra_producto.html', {'producto': producto})

# Vista para finalizar la compra
def finalizar_compra(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Aquí puedes agregar la lógica para procesar la compra
    # Por ejemplo, disminuir el stock, guardar la transacción, etc.
    
    # Vaciar el carrito después de la compra
    request.session['carrito'] = []

    messages.success(request, f'Compra de {producto.nombre} realizada con éxito.')
    return redirect('compra_exitosa', producto_id=producto.id)

# Vista para la compra exitosa
def compra_exitosa(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'productos/compra_exitosa.html', {'producto': producto})
