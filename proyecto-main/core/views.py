# core/views.py

from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required 

# Importa tus formularios, incluyendo el nuevo PerfilUsuarioForm
from .forms import RegistroClienteForm, LoginForm, PerfilUsuarioForm
# Importa tus modelos Usuario y los necesarios para las reservas
# Asegúrate de que 'Usuario' sea tu AUTH_USER_MODEL
from .models import Usuario, TipoUsuario, Reserva, DetalleReserva, Servicio, TipoServicio, EstadoReserva


# Vista para la página de inicio pública
def inicio(request):
    return render(request, 'core/inicio.html')

# Vista para el registro de usuarios
def registro(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '¡Su registro fue exitoso! Ahora puede iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroClienteForm()
    return render(request, 'core/registro.html', {'form': form})

# Vista para el inicio de sesión
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                auth_login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {user.nombre} {user.apellido}!')
                return redirect('inicioregistrado')
            else:
                messages.error(request, 'Ocurrió un error inesperado al iniciar sesión.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

# Vista para cerrar sesión
def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('inicio')

# Vista para la página de inicio de usuarios registrados
@login_required(login_url='login')
def inicioregistrado(request):
    return render(request, 'core/inicioregistrado.html')

# Resto de tus vistas
def hospedaje(request):
    return render (request, 'core/hospedaje.html')

def actividad(request):
    return render (request, 'core/actividad.html')

def gastronomia(request):
    return render (request, 'core/gastronomia.html')

def carrito(request):
    return render (request, 'core/carrito.html')


@login_required(login_url='login') # Asegura que solo usuarios autenticados puedan acceder
def perfil(request):
    usuario_actual = request.user
    form_submitted_with_errors = False # Para el JavaScript del frontend

    if request.method == 'POST':
        # Instancia el formulario con los datos POST y la instancia del usuario actual
        form = PerfilUsuarioForm(request.POST, instance=usuario_actual)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tus datos han sido actualizados correctamente!')
            # Después de guardar, redirige a la misma página para ver los datos actualizados
            return redirect('perfil')
        else:
            # Si el formulario no es válido, los errores se mostrarán en la plantilla
            messages.error(request, 'Hubo un error al actualizar tus datos. Por favor, revisa el formulario.')
            form_submitted_with_errors = True # Indicamos al JS que se envió el formulario con errores
    else:
        # Para una petición GET, instancia el formulario con los datos actuales del usuario
        form = PerfilUsuarioForm(instance=usuario_actual)

    # Lógica para "Mis Reservas"
    reservas_data = []
    # Las reservas solo se obtienen si el usuario es un cliente
    if usuario_actual.is_cliente: # Aquí usamos la propiedad is_cliente
        reservas_usuario = Reserva.objects.filter(usuario=usuario_actual).order_by('-fecha_reserva')
        
        # Prepara los datos de las reservas para mostrarlos en la tabla
        for reserva in reservas_usuario:
            servicios_reserva = DetalleReserva.objects.filter(reserva=reserva).select_related('servicio__tipo_servicio') # Optimizado con select_related
            
            # Recoge todos los nombres y tipos para concatenarlos
            nombres_servicios_list = []
            tipos_servicios_list = []
            for dr in servicios_reserva:
                nombres_servicios_list.append(dr.servicio.nombre)
                tipos_servicios_list.append(dr.servicio.tipo_servicio.nombre)

            # Usa set() para obtener nombres únicos y luego únelos con una coma
            nombres_servicios = ", ".join(sorted(list(set(nombres_servicios_list))))
            tipos_servicios = ", ".join(sorted(list(set(tipos_servicios_list))))

            reservas_data.append({
                'id': reserva.id,
                'tipo_servicio': tipos_servicios if tipos_servicios else 'N/A',
                'nombre_servicio': nombres_servicios if nombres_servicios else 'N/A',
                'fecha_inicio': reserva.fecha_inicio,
                'fecha_fin': reserva.fecha_fin,
                'estado_display': reserva.estado.estado if reserva.estado else 'Desconocido',
                'total': reserva.total,
            })

    context = {
        'form': form,
        'reservas': reservas_data, # Pasa las reservas procesadas
        'form_submitted': form_submitted_with_errors, # Pasa la bandera al template para el JS
        'user': usuario_actual, # Asegúrate de pasar el usuario al contexto
    }
    return render(request, 'core/perfil.html', context)

@login_required
def listar_servicios_anfitrion(request):
    # Esta vista también necesitará un filtro por anfitrión
    # Por ejemplo: servicios = Servicio.objects.filter(anfitrion=request.user)
    servicios = [] 
    context = {
        'servicios': servicios,
        'user': request.user, # Pasa el usuario para el navbar
    }
    return render(request, 'core/listar_servicios_anfitrion.html', context)

@login_required
def listar_reservas_anfitrion(request):
    # Aquí puedes filtrar las reservas para los servicios de este anfitrión
    # Ejemplo: reservas = Reserva.objects.filter(detallereserva__servicio__anfitrion=request.user).distinct()
    reservas_anfitrion = [] 
    context = {
        'reservas': reservas_anfitrion,
        'user': request.user, # Pasa el usuario para el navbar
    }
    return render(request, 'core/listar_reservas_anfitrion.html', context)