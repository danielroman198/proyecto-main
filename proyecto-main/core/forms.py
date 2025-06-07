from django import forms
from django.forms import ModelForm # Usa ModelForm directamente
from django.contrib.auth.hashers import make_password, check_password # Importar check_password para el login
from django.core.exceptions import ValidationError
from .models import Usuario, TipoUsuario # Asegúrate de que 'Usuario' y 'TipoUsuario' estén definidos en models.py

# Formulario de Registro de Cliente
class RegistroClienteForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirmar Contraseña')

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'password', 'telefono'] # Incluye 'telefono' aquí
        widgets = {
            # 'password': forms.PasswordInput(), # No es necesario repetir aquí si ya se define en el campo
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_correo(self):
        """
        Valida que el correo electrónico no esté ya registrado.
        """
        correo = self.cleaned_data.get('correo')
        if correo and Usuario.objects.filter(correo=correo).exists():
            raise ValidationError("Ya existe un usuario con este correo electrónico.")
        return correo

    def clean(self):
        """
        Valida que las contraseñas coincidan.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        """
        Guarda el usuario, hasheando la contraseña y asignando el rol 'cliente'.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Utiliza set_password que ya usa make_password internamente
        try:
            # Asigna el tipo de usuario 'cliente' por defecto al registrar
            tipo_cliente, created = TipoUsuario.objects.get_or_create(tipo_nombre='cliente') # get_or_create es más robusto
            user.tipo_usuario = tipo_cliente
        except Exception as e: # Captura cualquier excepción para dar un mensaje útil
            print(f"Advertencia: No se pudo asignar el TipoUsuario 'cliente'. Error: {e}")
            # Si quieres que el registro falle si el tipo de usuario no existe, puedes hacer:
            # raise ValidationError("Error en la configuración: El tipo de usuario 'cliente' no está definido.")

        if commit:
            user.save()
        return user

# Formulario de Inicio de Sesión (manteniendo tu implementación actual)
class LoginForm(forms.Form):
    correo = forms.EmailField(label='Correo Electrónico', max_length=254,
                              widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        """
        Valida las credenciales del usuario.
        """
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo')
        password = cleaned_data.get('password')

        if correo and password:
            try:
                user = Usuario.objects.get(correo=correo)
            except Usuario.DoesNotExist:
                # Si el correo no existe, lanza un error general para no dar pistas sobre usuarios existentes
                raise forms.ValidationError("Correo electrónico o contraseña incorrectos.")

            # Verifica la contraseña hasheada
            if not user.check_password(password): # Usa el método check_password de AbstractBaseUser
                raise forms.ValidationError("Correo electrónico o contraseña incorrectos.")

            # Si las credenciales son correctas, almacena el usuario en el formulario
            self.user_cache = user
        return cleaned_data

    def get_user(self):
        """
        Retorna la instancia del usuario autenticado.
        """
        return getattr(self, 'user_cache', None)

class PerfilUsuarioForm(ModelForm): 
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }