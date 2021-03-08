from dal import autocomplete
from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from clientes.models import Cliente
from presupuestos.constants import EstadoPresupuestos
from presupuestos.models import DetalleDePresupuesto, Presupuesto


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = '__all__'

        widgets = {
            "total": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }

    def __init__(self, *args, **kwargs):
        super(PresupuestoForm, self).__init__(*args, **kwargs)
        self.fields['total'].widget.attrs['readonly'] = True


class DetalleDePresupuestoForm(forms.ModelForm):
    class Meta:
        model = DetalleDePresupuesto
        fields = ('item', 'cantidad', 'precio_unitario', 'subtotal')

        widgets = {
           "item": autocomplete.Select2(url="item-autocomplete"),
            "subtotal": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }

    precio_unitario = forms.CharField(
        widget=forms.TextInput(
            attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.'}), label="Precio Unit.")

    def __init__(self, *args, **kwargs):
        super(DetalleDePresupuestoForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.initial['precio_unitario'] = instance.item.get_precio_unitario()
        self.fields['precio_unitario'].widget.attrs['readonly'] = True


class PresupuestoSearchForm(forms.Form):
    numero = forms.CharField(required=False,
                             widget=forms.TextInput(attrs={'placeholder': 'Número', 'style': 'width:120px;'}),
                             label="Número de presupuesto")
    obra = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Obra', 'style': 'width:220px;'}))
    cliente = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Cliente', 'style': 'width:220px;'}))
    ESTADO_EN_BLANCO = (('', '---------'),)
    estado = forms.ChoiceField(choices=ESTADO_EN_BLANCO + EstadoPresupuestos.ESTADOS, required=False)
    desde = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Desde'}), required=False)
    hasta = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Hasta'}), required=False)
