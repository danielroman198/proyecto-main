from django.shortcuts import redirect, render
from django.contrib import messages # Importa el módulo messages
from .forms import RegistroClienteForm

# Crea tus vistas aquí.

def inicio(request):
    return render(request, 'core/inicio.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            # Añade un mensaje de éxito
            messages.success(request, '¡Su registro fue exitoso! Ahora puede iniciar sesión.')
            return redirect('registro') # Redirige al nombre de la URL 'login'
    else:
        form = RegistroClienteForm()

    return render(request, 'core/registro.html', {'form': form})

def login(request):
    return render (request, 'core/login.html')

def hospedaje(request):
    return render (request, 'core/hospedaje.html')

def actividad(request):
    return render (request, 'core/actividad.html')

def gastronomia(request):
    return render (request, 'core/gastronomia.html')

def carrito(request):
    return render (request, 'core/carrito.html')

def inicioregistrado(request):
    return render (request, 'core/inicioregistrado.html')

def perfil(request):
    return render (request, 'core/perfil.html')
