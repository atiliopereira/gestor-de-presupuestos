from django.contrib.auth.models import User
from django.db import models

from sistema.constants import TipoDeUsuario


class Departamento(models.Model):
    class Meta:
        verbose_name_plural = "Departamentos"
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre}'


class Ciudad(models.Model):
    class Meta:
        verbose_name_plural = "Ciudades"
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.nombre}'


class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    ruc = models.CharField(max_length=20, verbose_name="RUC/CI Nro.", null=True, blank=True)
    tipo_de_usuario = models.CharField(max_length=2, choices=TipoDeUsuario.TIPOS, default=TipoDeUsuario.PERSONA)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
    logo = models.ImageField(blank=True, null=True)


def get_ciudad_default():
    ciudad_principal = Ciudad.objects.get(pk=1)
    if ciudad_principal:
        return ciudad_principal.pk
    else:
        return Ciudad.objects.create(nombre='Asunción').pk
