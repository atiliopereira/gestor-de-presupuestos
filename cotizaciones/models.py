import datetime

from django.contrib.auth.models import User
from django.db import models

from cotizaciones.constants import TiposDeCotizacion, EstadoDeSolicitud
from materiales.models import Material
from presupuestos.models import Presupuesto, DetalleDePresupuesto
from profesionales.models import Proveedor, Profesional
from servicios.models import Servicio


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
    estado = models.CharField(max_length=2, choices=EstadoDeSolicitud.ESTADOS, default=EstadoDeSolicitud.VIGENTE)

    def __str__(self):
        return f'Solicitud de cotización {self.pk} - {self.presupuesto.numero_de_presupuesto}'

    def get_ciudad(self):
        return f'{self.presupuesto.ciudad.nombre}'
    get_ciudad.short_description = 'Ciudad'

    def get_cotizaciones(self):
        return Cotizacion.objects.filter(solicitud=self).count()
    get_cotizaciones.short_description = "Cotizaciones recibidas"


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
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT, editable=False)


class MaterialDeCotizacion(models.Model):
    class Meta:
        verbose_name_plural = "Materiales de la Cotizaciones"
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name="Precio Unitario",
                                 help_text="Indicar el precio unitario")


class ServicioDeCotizacion(models.Model):
    class Meta:
        verbose_name_plural = "Servicios de la Cotizaciones"
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name="Precio Unitario",
                                 help_text="Indicar el precio unitario")
