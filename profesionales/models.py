from django.db import models


class Servicio(models.Model):
    descripcion = models.CharField(max_length=150, verbose_name="descripción")
    activo = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return f'{self.descripcion}'


class Profesional(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre o Razón social")
    ruc = models.CharField(max_length=20, verbose_name="RUC", null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name="dirección")
    telefono = models.CharField(max_length=50, null=True, blank=True, verbose_name="teléfono")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="e-mail")

    def __str__(self):
        return f'{self.nombre}'


class ServicioProfesional(models.Model):
    profesional = models.ForeignKey(Profesional, on_delete=models.PROTECT)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)

