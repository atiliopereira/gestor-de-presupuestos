from django.db import models


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
