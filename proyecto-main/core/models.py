from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.utils import IntegrityError # Importar para manejar errores de integridad


# Manager para tu modelo de usuario personalizado
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el correo electrónico y la contraseña dados.
        """
        if not correo:
            raise ValueError('El correo electrónico es obligatorio')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password) # set_password hashea la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con el correo electrónico y la contraseña dados.
        Asigna automáticamente el rol 'administrador' si existe.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Intenta asignar el TipoUsuario 'administrador'
        try:
            # get_or_create es útil: si existe, lo obtiene; si no, lo crea.
            tipo_admin, created = TipoUsuario.objects.get_or_create(tipo_nombre='administrador')
            extra_fields.setdefault('tipo_usuario', tipo_admin)
            if created:
                print("Se ha creado automáticamente el TipoUsuario 'administrador' al crear el superusuario.")
        except Exception as e:
            print(f"Advertencia: No se pudo asignar el TipoUsuario 'administrador' al superusuario. Error: {e}")
            print("Asegúrate de que el TipoUsuario 'administrador' exista o créalo manualmente en el admin.")
            # Si hay un error, el superusuario se creará sin tipo_usuario asignado,
            # pero seguirá siendo superusuario por is_superuser=True.

        return self.create_user(correo, password, **extra_fields)

# Modelo para los tipos de usuario (roles)
class TipoUsuario(models.Model):
    tipo_nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Tipo de Usuario"
        verbose_name_plural = "Tipos de Usuarios"

    def __str__(self):
        return self.tipo_nombre

# Tu modelo de usuario personalizado
class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True) # Campo de teléfono
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True) # Indica si la cuenta está activa
    is_staff = models.BooleanField(default=False) # Necesario para acceder al admin de Django
    date_joined = models.DateTimeField(auto_now_add=True) # Fecha de creación del usuario

    objects = UsuarioManager() # Asigna tu Manager personalizado

    USERNAME_FIELD = 'correo' # Django usará 'correo' como campo de nombre de usuario para el login
    REQUIRED_FIELDS = ['nombre', 'apellido'] # Campos requeridos al crear un superusuario con createsuperuser

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.correo})"

    # Métodos necesarios para la compatibilidad con el sistema de autenticación de Django
    def get_full_name(self):
        """
        Retorna el nombre completo del usuario.
        """
        return f"{self.nombre} {self.apellido}"

    def get_short_name(self):
        """
        Retorna el nombre corto del usuario.
        """
        return self.nombre

    def has_perm(self, perm, obj=None):
        """
        Indica si el usuario tiene un permiso específico.
        Los superusuarios siempre tienen todos los permisos.
        """
        if self.is_active and self.is_superuser:
            return True
        # Aquí podrías añadir lógica más granular basada en roles o permisos específicos
        # Por ejemplo: if self.tipo_usuario.tipo_nombre == 'administrador': return True
        return self.user_permissions.filter(codename=perm.split('.')[-1]).exists()

    def has_module_perms(self, app_label):
        """
        Indica si el usuario tiene permisos para ver la aplicación `app_label`.
        Los superusuarios siempre tienen permisos para todos los módulos.
        """
        if self.is_active and self.is_superuser:
            return True
        return True

# --- Otros modelos de tu proyecto (mantén los que ya tienes) ---
# Asegúrate de que estos modelos también estén correctamente definidos

class TipoServicio(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    anfitrion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='servicios_ofrecidos')

    def __str__(self):
        return self.nombre

class EstadoReserva(models.Model):
    estado = models.CharField(max_length=50)
    def __str__(self):
        return self.estado

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.ForeignKey(EstadoReserva, on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reserva {self.id} - {self.usuario.correo}"

class DetalleReserva(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de Reserva {self.reserva.id} - {self.servicio.nombre}"

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Carrito de {self.usuario.correo}"

class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"Item en carrito {self.carrito.id} - {self.servicio.nombre}"

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class EstadoPago(models.Model):
    estado = models.CharField(max_length=50)
    def __str__(self):
        return self.estado

class Pago(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)
    estado_pago = models.ForeignKey(EstadoPago, on_delete=models.SET_NULL, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.id} - {self.reserva.usuario.correo}"
