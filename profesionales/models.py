from django.db import models

from materiales.models import Material
from servicios.models import Servicio
from sistema.models import Ciudad


class Profesional(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre o Razón social")
    ruc = models.CharField(max_length=20, verbose_name="RUC", null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name="dirección")
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT, blank=True, null=True)
    telefono = models.CharField(max_length=50, null=True, blank=True, verbose_name="teléfono")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="e-mail")

    def __str__(self):
        return f'{self.nombre}'

    def get_servicios(self):
        servicios = [s.servicio.descripcion for s in ServicioProfesional.objects.filter(profesional=self)]
        if servicios:
            return ', '.join(servicios)
        else:
            return f'Ningún servicio registrado'
    get_servicios.short_description = "Servicios Prestados"


class ServicioProfesional(models.Model):
    profesional = models.ForeignKey(Profesional, on_delete=models.PROTECT)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre o Razón social")
    ruc = models.CharField(max_length=20, verbose_name="RUC", null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name="dirección")
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT, blank=True, null=True)
    telefono = models.CharField(max_length=50, null=True, blank=True, verbose_name="teléfono")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="e-mail")

    def __str__(self):
        return f'{self.nombre}'

    def get_materiales(self):
        materiales = [m.material.descripcion for m in MaterialProveedor.objects.filter(proveedor=self)]
        if materiales:
            return ', '.join(materiales)
        else:
            return f'Ningún material registrado'
    get_materiales.short_description = "Materiales"


class MaterialProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)