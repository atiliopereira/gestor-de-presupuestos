import datetime
import re

from django.db import models

from clientes.models import Cliente
from items.models import Item, MaterialDeItem, ServicioDeItem
from materiales.models import Material
from presupuestos.constants import EstadoPresupuestos
from sistema.models import Ciudad


class Presupuesto(models.Model):
    fecha = models.DateField(default=datetime.date.today)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    numero_de_presupuesto = models.CharField(max_length=100, verbose_name="Número de presupuesto", editable=False)
    obra = models.CharField(max_length=250, help_text="Nombre o Descripción")
    direccion = models.CharField(max_length=300, verbose_name="Dirección", blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT, null=True, blank=True)
    estado = models.CharField(max_length=3, choices=EstadoPresupuestos.ESTADOS, default=EstadoPresupuestos.PENDIENTE, editable=False)
    total = models.DecimalField(max_digits=15, decimal_places=0, default=0)

    def __str__(self):
        return f'Presupuesto Nº {self.numero_de_presupuesto} - {self.obra} ({self.cliente.nombre})'

    def get_lista_de_recursos(self):
        result = {}
        detalles_de_presupuesto = DetalleDePresupuesto.objects.filter(presupuesto=self)
        for dp in detalles_de_presupuesto:
            for mi in MaterialDeItem.objects.filter(item=dp.item):
                clave = f'm{mi.material.pk}'
                if clave not in result:
                    result[clave] = float(dp.cantidad) * mi.coeficiente
                else:
                    valor_anterior = result[clave]
                    result[clave] = valor_anterior + float(dp.cantidad) * mi.coeficiente

            for si in ServicioDeItem.objects.filter(item=dp.item):
                clave = f's{si.servicio.pk}'
                if clave not in result:
                    result[clave] = float(dp.cantidad) * si.coeficiente
                else:
                    valor_anterior = result[clave]
                    result[clave] = valor_anterior + float(dp.cantidad) * si.coeficiente
        return result


class DetalleDePresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    cantidad = models.FloatField(default=1)
    subtotal = models.DecimalField(max_digits=15, decimal_places=0, default=0)

    def get_recursos_de_detalle(self):
        materiales = [[mi.material.descripcion, mi.coeficiente * self.cantidad, mi.material.unidad_de_medida.simbolo] for mi in
                      MaterialDeItem.objects.filter(item=self.item)]
        servicios = [[si.servicio.descripcion, si.coeficiente * self.cantidad, si.servicio.unidad_de_medida.simbolo] for si in
                      ServicioDeItem.objects.filter(item=self.item)]
        return materiales, servicios


def get_siguiente_numero_de_presupuesto(user):
    anho = datetime.date.today().year
    ultimo_presupuesto = Presupuesto.objects.filter(cliente__creado_por=user).filter(fecha__year=anho) \
      .extra(select={"num" : "COALESCE(CAST(SUBSTRING(numero_de_presupuesto FROM '^[0-9]+') AS INTEGER), -1)"}) \
      .order_by("num", "numero_de_presupuesto").last()
    numero = 1

    if ultimo_presupuesto:
        match = re.search("^\d+", ultimo_presupuesto.numero_de_presupuesto)

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
