from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from django import forms

from sistema.models import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('ruc', 'tipo_de_usuario', 'ciudad', 'logo')

    def clean(self):
        logo = self.cleaned_data.get("logo")
        if logo:
            w, h = get_image_dimensions(logo)
            if w != h:
                raise forms.ValidationError("La imagen debe ser cuadrada, de máximo 720x720 px")
            if w > 720:
                raise forms.ValidationError("La imagen es %i pixels de ancho. El máximo permitido es 720px" % w)
            if h > 720:
                raise forms.ValidationError("La imagen es %i pixels de alto. El máximo permitido es 720px" % h)


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )
