import datetime

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
