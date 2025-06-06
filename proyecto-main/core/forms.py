from django import forms
from django.forms import ModelForm
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
            'password': forms.PasswordInput(),
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
        confirm_password = cleaned = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        """
        Guarda el usuario, hasheando la contraseña y asignando el rol 'cliente'.
        """
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"]) # Hashea la contraseña antes de guardar
        try:
            # Asigna el tipo de usuario 'cliente' por defecto al registrar
            tipo_cliente = TipoUsuario.objects.get(tipo_nombre='cliente')
            user.tipo_usuario = tipo_cliente
        except TipoUsuario.DoesNotExist:
            print("Error: El tipo de usuario 'cliente' no existe. Asegúrate de crearlo en la base de datos.")
            raise # Vuelve a lanzar la excepción para que Django la maneje

        if commit:
            user.save()
        return user

# Formulario de Inicio de Sesión
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
            if not check_password(password, user.password):
                raise forms.ValidationError("Correo electrónico o contraseña incorrectos.")

            # Si las credenciales son correctas, almacena el usuario en el formulario
            self.user_cache = user
        return cleaned_data

    def get_user(self):
        """
        Retorna la instancia del usuario autenticado.
        """
        return getattr(self, 'user_cache', None)
