from django.db import models
from materiales.models import UnidadDeMedida, Material


class Rubro(models.Model):
    nombre = nombre = models.CharField(max_length = 200)

    def __str__(self):
        return f'{self.nombre}'


class Item(models.Model):
    class Meta:
        verbose_name = "ítem"
        verbose_name_plural = "ítems"

    rubro = models.ForeignKey(Rubro, on_delete = models.PROTECT)
    descripcion = models.CharField(max_length = 200, verbose_name = "descripción")
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.descripcion}'


class DetalleDeItem(models.Model):
    class Meta:
        verbose_name = "detalle de ítem"
        verbose_name_plural = "detalles de ítem"

    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    material = models.ForeignKey(Material, on_delete = models.PROTECT)
    coeficiente = models.FloatField(default = 1.0)

    def __str__(self):
        return f'{self.item}'
