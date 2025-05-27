from django.db import models




class TipoUsuario(models.Model):
    """Represents the type of user (e.g., cliente, anfitrión, administrador)."""
    tipo_nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo_nombre


class Usuario(models.Model):
    """Stores user information."""
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Renamed from contrasena
    telefono = models.CharField(max_length=10)
    fecha_registro = models.DateField(auto_now_add=True)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.correo} {self.telefono} {self.fecha_registro} {self.tipo_usuario}"

class TipoServicio(models.Model):
    """Categorizes services (e.g., hospedaje, actividad, gastronomía)."""
    tipo_nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo_nombre


class Servicio(models.Model):
    """Represents a service offered (e.g., a tour, a hotel room)."""
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(255)
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.PROTECT)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    ubicacion = models.CharField(max_length=255)
    imagen_url = models.URLField(max_length=2000)
    anfitrion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='servicios_ofrecidos')

    def __str__(self):
        return self.nombre


class EstadoReserva(models.Model):
    """Tracks the status of a reservation (e.g., pendiente, confirmada)."""
    estado_nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.estado_nombre


class Reserva(models.Model):
    """A user's reservation for a service."""
    fecha_reserva = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado_reserva = models.ForeignKey(EstadoReserva, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas')

    def __str__(self):
        return f"Reserva {self.id} - {self.usuario}"


class DetalleReserva(models.Model):
    """Details of the services included in a reservation."""
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='detalles')
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle Reserva {self.id} - {self.servicio.nombre}"


class Carrito(models.Model):
    """Shopping cart for a user."""
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='carrito')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario}"


class DetalleCarrito(models.Model):
    """Items in the shopping cart."""
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='detalles')
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle Carrito {self.id} - {self.servicio.nombre}"


class MetodoPago(models.Model):
    """Payment methods (e.g., Transbank, WebPay)."""
    metodo_nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.metodo_nombre


class EstadoPago(models.Model):
    """Payment statuses (e.g., completado, pendiente)."""
    estado_nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.estado_nombre


class Pago(models.Model):
    """Payment information for a reservation."""
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.ForeignKey(EstadoPago, on_delete=models.PROTECT)
    transaccion_id = models.CharField(max_length=255)

    def __str__(self):
        return f"Pago {self.id} - Reserva {self.reserva.id}"