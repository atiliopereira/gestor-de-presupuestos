import datetime

from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from cotizaciones.constants import TiposDeCotizacion
from cotizaciones.models import Solicitud, MaterialDeSolicitud, ServicioDeSolicitud
from sistema.models import Ciudad


class SolicitudDeCotizacionForm(forms.Form):
    vencimiento = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y',
                                                         attrs={'class': 'form-control', 'placeholder': 'Selecccionar Fecha',
                                                                'type': 'date'}), )
    comentarios = forms.CharField(widget=forms.Textarea(
        attrs={'style': 'text-align:left', 'size': '40', 'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','}),
        required=False, help_text="Comentarios o indicaciones adicionales")


class SolicitudSearchForm(forms.Form):
    ESTADO_EN_BLANCO = (('', '---------'),)
    tipo = forms.ChoiceField(choices=ESTADO_EN_BLANCO + TiposDeCotizacion.TIPOS, required=False)
    ciudad = forms.ModelChoiceField(required=False, queryset=Ciudad.objects.all(), label='Ciudad', widget=forms.Select)
    desde = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'dd/mm/aaaa'}), label='Vencimiento desde', required=False)
    hasta = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'dd/mm/aaaa'}), required=False)


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SolicitudForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs['readonly'] = True


class MaterialDeSolicitudForm(forms.ModelForm):
    class Meta:
        model = MaterialDeSolicitud
        fields = ('material', 'cantidad',)

        widgets = {
            "cantidad": forms.TextInput(attrs={
                'style': 'text-align:right', 'size': '10',
                'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','
            }),
        }


class ServicioDeSolicitudForm(forms.ModelForm):
    class Meta:
        model = ServicioDeSolicitud
        fields = ('servicio', 'cantidad',)

        widgets = {
            "cantidad": forms.TextInput(attrs={
                'style': 'text-align:right', 'size': '10',
                'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','
            }),
        }
