import datetime

from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from cotizaciones.constants import TiposDeCotizacion
from cotizaciones.models import Solicitud, Cotizacion, MaterialDeCotizacion, ServicioDeCotizacion
from materiales.models import Material
from servicios.models import Servicio
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
        self.fields['presupuesto'].widget.attrs['readonly'] = True
        self.fields['tipo'].widget.attrs['readonly'] = True


class MaterialDeCotizacionForm(forms.ModelForm):
    cantidad = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'text-align:right', 'size': '6', 'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','}),
        required=False, )

    class Meta:
        model = MaterialDeCotizacion
        fields = ('material', 'cantidad', 'precio')

        widgets = {
            "precio": forms.TextInput(attrs={
                'style': 'text-align:right', 'size': '20',
                'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','
            }),
        }

    def __init__(self, *args, **kwargs):
        super(MaterialDeCotizacionForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            search_key = f'm{instance.material.pk}'
            items = [item for item in instance.cotizacion.solicitud.presupuesto.get_lista_de_recursos().items() if
                     item[0] == search_key]
            # El list resultante deberia devolver solamente un valor
            cantidad = items[0][1] if len(items) == 1 else 0
            id_material = int(items[0][0][1:])
            material = Material.objects.get(id=id_material)

            self.initial['cantidad'] = f'{cantidad} {material.unidad_de_medida.simbolo.lower()}'

        self.fields['material'].widget.attrs['readonly'] = True
        self.fields['cantidad'].widget.attrs['readonly'] = True


class ServicioDeCotizacionForm(forms.ModelForm):
    cantidad = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'text-align:right', 'size': '6', 'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','}),
        required=False, )

    class Meta:
        model = ServicioDeCotizacion
        fields = ('servicio', 'cantidad', 'precio')

        widgets = {
            "precio": forms.TextInput(attrs={
                'style': 'text-align:right', 'size': '20',
                'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ServicioDeCotizacionForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            search_key = f'm{instance.servicio.pk}'
            items = [item for item in instance.cotizacion.solicitud.presupuesto.get_lista_de_recursos().items() if
                     item[0] == search_key]
            # El list resultante deberia devolver solamente un valor
            cantidad = items[0][1] if len(items) == 1 else 0
            id_servicio = int(items[0][0][1:])
            servicio = Servicio.objects.get(id=id_servicio)

            self.initial['cantidad'] = f'{cantidad} {servicio.unidad_de_medida.simbolo.lower()}'

        self.fields['servicio'].widget.attrs['readonly'] = True
        self.fields['cantidad'].widget.attrs['readonly'] = True


class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CotizacionForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs['readonly'] = True
        self.fields['solicitud'].widget.attrs['readonly'] = True

