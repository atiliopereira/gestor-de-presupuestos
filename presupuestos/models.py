import datetime
import re

from django.db import models

from clientes.models import Cliente
from items.models import Item
from presupuestos.constants import EstadoPresupuestos
from sistema.models import Ciudad


class Presupuesto(models.Model):
    fecha = models.DateField(default=datetime.date.today)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    numero_de_presupuesto = models.CharField(max_length=100, verbose_name="Número de presupuesto")
    obra = models.CharField(max_length=250, verbose_name="Nombre o Descripción")
    direccion = models.CharField(max_length=300, verbose_name="Dirección", blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT, null=True, blank=True)
    estado = models.CharField(max_length=3, choices=EstadoPresupuestos.ESTADOS, default=EstadoPresupuestos.PENDIENTE, editable=False)
    total = models.DecimalField(max_digits=15, decimal_places=0, default=0)

    def __str__(self):
        return f'Presupuesto Nº{self.numero_de_presupuesto} - {self.obra} ({self.cliente.nombre})'


class DetalleDePresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    cantidad = models.FloatField(default=1)
    subtotal = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    

def get_siguiente_numero_de_presupuesto():
    anho = datetime.date.today().year
    query_set = Presupuesto.objects.filter(fecha__year=anho).order_by("-pk")[:1]
    numero = 0

    if len(query_set) == 1:
        match = re.search("^\d+", query_set[0].numero_de_presupuesto)

        if match:
            numero = int(match.group()) + 1

    return "{:#04d}-00/{:#d}".format(numero, anho)

def get_siguiente_numero_de_revision(numero_de_presupuesto):
    match = re.search("-\d+", numero_de_presupuesto)

    if match:
        prefijo = numero_de_presupuesto[:match.start()]
        sufijo  = numero_de_presupuesto[match.end():]
        num_revision = int(match.group()[1:]) + 1
        numero_de_presupuesto = "{}-{:#02d}{}".format(prefijo, num_revision, sufijo)

    return numero_de_presupuesto
    