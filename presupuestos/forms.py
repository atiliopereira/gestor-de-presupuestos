from dal import autocomplete
from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from items.models import get_precio_unitario_de_item
from presupuestos.constants import EstadoPresupuestos
from presupuestos.models import DetalleDePresupuesto, Presupuesto, AdicionalDePresupuesto
from tillner.globales import separar


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = '__all__'

        widgets = {
            "total": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }

    total_con_ganancia = forms.CharField(
        widget=forms.TextInput(
            attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.'}),
        label="Total con Ganancia", initial=0)

    def __init__(self, *args, **kwargs):
        super(PresupuestoForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.initial['total_con_ganancia'] = separar(round(instance.total_mas_ganancia))
            self.initial['total'] = round(instance.total)
        self.fields['total_con_ganancia'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True


class DetalleDePresupuestoForm(forms.ModelForm):
    class Meta:
        model = DetalleDePresupuesto
        fields = ('item', 'cantidad', 'precio_unitario', 'subtotal')
        localized_fields = ('precio_unitario', 'subtotal',)

        widgets = {
           "item": autocomplete.Select2(url="item-autocomplete", forward=['ciudad'],
                                        attrs={'data-dropdown-auto-width': 'true', 'style': "width: 100%;"}),
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
            self.initial['precio_unitario'] = round(
                get_precio_unitario_de_item(instance.item, instance.presupuesto.ciudad))
        self.fields['precio_unitario'].widget.attrs['readonly'] = True
        self.fields['subtotal'].widget.attrs['readonly'] = True


class AdicionalDePresupuestoForm(forms.ModelForm):
    class Meta:
        model = AdicionalDePresupuesto
        fields = '__all__'
        localized_fields = ('subtotal',)

        widgets = {
            "descripcion": forms.TextInput(attrs={'placeholder': 'Descripción del item', 'style': 'text-align:left', 'size': '70', 'class': 'auto'}),
            "precio_unitario": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }

    subtotal = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.'}),
        label="Subtotal", help_text='cant x precio unit.', initial=0)

    def __init__(self, *args, **kwargs):
        super(AdicionalDePresupuestoForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.initial['subtotal'] = separar(round(instance.subtotal))
        self.fields['subtotal'].widget.attrs['readonly'] = True


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
