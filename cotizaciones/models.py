import datetime

from django.contrib.auth.models import User
from django.db import models

from cotizaciones.constants import TiposDeCotizacion
from presupuestos.models import Presupuesto, DetalleDePresupuesto
from profesionales.models import Proveedor, Profesional


def get_vencimiento_defautl():
    return datetime.date.today() + datetime.timedelta(days=8)


class Solicitud(models.Model):
    class Meta:
        verbose_name = "Solicitud de Cotización"
        verbose_name_plural = "Solicitudes de cotización"
        unique_together = ('presupuesto', 'tipo',)

    fecha = models.DateField(default=datetime.date.today)
    vencimiento = models.DateField(default=get_vencimiento_defautl)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=1, choices=TiposDeCotizacion.TIPOS, default=TiposDeCotizacion.MATERIAL)
    comentarios = models.TextField(max_length=1000, blank=True, null=True)
    proveedores = models.ManyToManyField(Proveedor, blank=True,
                                         help_text="Los proveedores seleccionados serán notificados de la solicitud de cotización")
    profesionales = models.ManyToManyField(Profesional, blank=True,
                                         help_text="Los profesionales seleccionados serán notificados de la solicitud de cotización")

    def __str__(self):
        return f'Solicitud de cotización {self.pk} - {self.presupuesto.numero_de_presupuesto}'

    def get_ciudad(self):
        return f'{self.presupuesto.ciudad.nombre}'
    get_ciudad.short_description = 'Ciudad'


class DetalleDeSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    detalle_de_presupuesto = models.ForeignKey(DetalleDePresupuesto, on_delete=models.CASCADE)


class Cotizacion(models.Model):
    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
    fecha = models.DateField(default=datetime.date.today)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='cotizaciones', null=True, blank=True)
    comentarios = models.TextField(max_length=1000, blank=True, null=True)