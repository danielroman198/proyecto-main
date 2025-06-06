from django.urls import path
from . import views # Importa tus vistas desde el mismo directorio

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'), # Usa tu propia vista de logout
    path('hospedaje/', views.hospedaje, name='hospedaje'),
    path('actividad/', views.actividad, name='actividad'),
    path('gastronomia/', views.gastronomia, name='gastronomia'),
    path('carrito/', views.carrito, name='carrito'),
    path('inicioregistrado/', views.inicioregistrado, name='inicioregistrado'),
    path('perfil/', views.perfil, name='perfil'),
    path('listar_servicios_anfitrion', views.listar_servicios_anfitrion, name='listar_servicios_anfitrion'),
    path('listar_reservas_anfitrion', views.listar_reservas_anfitrion, name='listar_reservas_anfitrion')
]
