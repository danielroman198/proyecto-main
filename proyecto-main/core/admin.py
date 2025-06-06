from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(TipoUsuario)
admin.site.register(Usuario)
admin.site.register(TipoServicio)
admin.site.register(Servicio)
admin.site.register(EstadoReserva)
admin.site.register(Reserva)
admin.site.register(DetalleReserva)
admin.site.register(Carrito)
admin.site.register(DetalleCarrito)
admin.site.register(MetodoPago)
admin.site.register(EstadoPago)
admin.site.register(Pago)
