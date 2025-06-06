from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required # Importar para proteger vistas

from .forms import RegistroClienteForm, LoginForm # Importa tu LoginForm
from .models import Usuario, TipoUsuario # Importa tus modelos Usuario y TipoUsuario

# Vista para la página de inicio pública
def inicio(request):
    return render(request, 'core/inicio.html')

# Vista para el registro de usuarios
def registro(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save() # Guarda el usuario y obtén la instancia
            messages.success(request, '¡Su registro fue exitoso! Ahora puede iniciar sesión.')
            # Redirige a la página de login después de un registro exitoso
            return redirect('login') # ¡CORREGIDO! Redirige a la URL con nombre 'login'
    else:
        form = RegistroClienteForm()

    return render(request, 'core/registro.html', {'form': form})

# Vista para el inicio de sesión
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) # Instancia tu LoginForm con los datos enviados
        if form.is_valid():
            # El formulario ya ha verificado el correo y la contraseña
            user = form.get_user() # Obtiene la instancia del usuario autenticado
            if user:
                # Usa la función login de Django para establecer la sesión del usuario
                auth_login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {user.nombre} {user.apellido}!')
                # Redirige a la página de inicio para usuarios registrados
                return redirect('inicioregistrado')
            else:
                # Esto no debería ocurrir si form.is_valid() es True y get_user() devuelve None
                messages.error(request, 'Ocurrió un error inesperado al iniciar sesión.')
        else:
            # Si el formulario no es válido, los errores se mostrarán automáticamente en la plantilla
            # No es necesario añadir un messages.error aquí, ya que el formulario maneja la validación
            pass
    else:
        form = LoginForm() # Instancia un formulario vacío para peticiones GET

    return render(request, 'core/login.html', {'form': form})

# Vista para cerrar sesión
def logout_view(request):
    auth_logout(request) # Cierra la sesión del usuario actual
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('inicio') # Redirige a la página de inicio pública después de cerrar sesión

# Vista para la página de inicio de usuarios registrados
# @login_required(login_url='login') asegura que solo usuarios autenticados puedan acceder.
# Si un usuario no autenticado intenta acceder, será redirigido a la URL con nombre 'login'.
@login_required(login_url='login')
def inicioregistrado(request):
    # Cuando un usuario está autenticado, Django automáticamente hace que el objeto 'request.user'
    # esté disponible en el contexto de la plantilla. 'request.user' será una instancia de tu modelo Usuario.
    return render(request, 'core/inicioregistrado.html') # No necesitas pasar 'user' explícitamente aquí

# Resto de tus vistas (puedes protegerlas con @login_required si es necesario)
def hospedaje(request):
    return render (request, 'core/hospedaje.html')

def actividad(request):
    return render (request, 'core/actividad.html')

def gastronomia(request):
    return render (request, 'core/gastronomia.html')

def carrito(request):
    return render (request, 'core/carrito.html')

def perfil(request):
    # También puedes proteger esta vista si es solo para usuarios logueados
    # @login_required(login_url='login')
    return render (request, 'core/perfil.html')

@login_required
def listar_servicios_anfitrion(request):
    # Aquí iría la lógica para obtener los servicios del anfitrión
    # Por ejemplo, si tienes un modelo llamado 'Servicio':
    # servicios = Servicio.objects.filter(anfitrion=request.user)
    servicios = [] # Placeholder por ahora

    context = {
        'servicios': servicios,
    }
    return render(request, 'core/listar_servicios_anfitrion.html', context)

@login_required
def listar_reservas_anfitrion(request):
    # Aquí iría la lógica para obtener los servicios del anfitrión
    # Por ejemplo, si tienes un modelo llamado 'Servicio':
    # servicios = Servicio.objects.filter(anfitrion=request.user)
    servicios = [] # Placeholder por ahora

    context = {
        'servicios': servicios,
    }
    return render(request, 'core/listar_reservas_anfitrion.html', context)

