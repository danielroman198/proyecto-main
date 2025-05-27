from django import forms
from django.forms import ModelForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .models import Usuario, TipoUsuario # Asegúrate de que 'Usuario' y 'TipoUsuario' estén definidos en models.py

class RegistroClienteForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirmar Contraseña')

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'password', 'telefono'] # 'password' se maneja manualmente para hashing
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_correo(self):
        correo = self.cleaned_data.get('correo') # Usar .get() para evitar KeyError si el campo no está presente
        if correo and Usuario.objects.filter(correo=correo).exists():
            raise ValidationError("Ya existe un usuario con este correo electrónico.")
        return correo

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.") # Asocia el error a un campo específico
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"]) # Hashea la contraseña
        try:
            tipo_cliente = TipoUsuario.objects.get(tipo_nombre='cliente')
            user.tipo_usuario = tipo_cliente
        except TipoUsuario.DoesNotExist:
            # Es importante manejar este error; podrías loggearlo o crear el tipo de usuario si no existe
            print("Error: El tipo de usuario 'cliente' no existe. Asegúrate de crearlo en la base de datos.")
            raise # Vuelve a lanzar la excepción para que Django la maneje
        if commit:
            user.save()
        return user
