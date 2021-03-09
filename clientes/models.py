from django.contrib.auth.models import User
from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre o Razón social")
    ruc = models.CharField(max_length=20, verbose_name="RUC", null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name="dirección")
    telefono = models.CharField(max_length=50, null=True, blank=True, verbose_name="teléfono")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="e-mail")
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT, editable=False)

    def __str__(self):
        return f'{self.nombre}'

    def get_propietario(self):
        return self.creado_por
