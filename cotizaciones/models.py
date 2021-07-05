import datetime

from django.contrib.auth.models import User
from django.db import models

from cotizaciones.constants import TiposDeCotizacion, EstadoDeSolicitud
from materiales.models import Material
from presupuestos.models import Presupuesto, DetalleDePresupuesto
from profesionales.models import Proveedor, Profesional
from servicios.models import Servicio
from sistema.models import Ciudad


def get_vencimiento_defautl():
    return datetime.date.today() + datetime.timedelta(days=8)


class Solicitud(models.Model):
    class Meta:
        verbose_name = "Solicitud de Cotización"
        verbose_name_plural = "Solicitudes de cotización"

    fecha = models.DateField(default=datetime.date.today)
    vencimiento = models.DateField(default=get_vencimiento_defautl)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=1, choices=TiposDeCotizacion.TIPOS, default=TiposDeCotizacion.MATERIAL)
    comentarios = models.TextField(max_length=1000, blank=True, null=True)
    archivo = models.FileField(upload_to='cotizaciones', null=True, blank=True, help_text="Graficos, tablas o especificaciones adicionales.")
    estado = models.CharField(max_length=2, choices=EstadoDeSolicitud.ESTADOS, default=EstadoDeSolicitud.VIGENTE,
                              editable=False)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT, editable=False)

    def __str__(self):
        return f'Solicitud de cotización {self.pk} ({self.get_estado_display()})'


class MaterialDeSolicitud(models.Model):
    class Meta:
        verbose_name_plural = "Materiales de la Solicitud"
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=7, decimal_places=2)


class ServicioDeSolicitud(models.Model):
    class Meta:
        verbose_name_plural = "Servicios de la Solicitud"
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=7, decimal_places=2)
