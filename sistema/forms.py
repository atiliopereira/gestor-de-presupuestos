from django.core.files.images import get_image_dimensions
from django import forms

from sistema.models import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

    def clean(self):
        logo = self.cleaned_data.get("logo")
        if not logo:
            raise forms.ValidationError("No image!")
        else:
            w, h = get_image_dimensions(logo)
            if w != h:
                raise forms.ValidationError("La imagen debe ser cuadrada, de máximo 720x720 px")
            if w > 720:
                raise forms.ValidationError("La imagen es %i pixels de ancho. El máximo permitido es 720px" % w)
            if h > 720:
                raise forms.ValidationError("La imagen es %i pixels de alto. El máximo permitido es 720px" % h)
