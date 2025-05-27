from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),
    path('hospedaje/', views.hospedaje, name='hospedaje'),
    path('actividad/', views.actividad, name='actividad'),
    path('gastronomia/', views.gastronomia, name='gastronomia'),
    path('carrito/', views.carrito, name='carrito'),
    path('inicioregistrado/', views.inicioregistrado, name='inicioregistrado'),
    path('perfil/', views.perfil, name='perfil'),
]