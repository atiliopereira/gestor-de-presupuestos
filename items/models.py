from django.db import models
from materiales.models import UnidadDeMedida, Material, get_precio_de_material
from servicios.models import Servicio, get_precio_de_servicio


class Rubro(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.nombre}'


class Item(models.Model):
    class Meta:
        verbose_name = "ítem"
        verbose_name_plural = "ítems"

    rubro = models.ForeignKey(Rubro, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=200, verbose_name="descripción")
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.descripcion} ({self.rubro})'


def get_precio_unitario_de_item(item, ciudad):
    total_materiales = total_servicios = 0
    detalles_de_materiales = MaterialDeItem.objects.filter(item=item)
    for dm in detalles_de_materiales:
        precio_de_material = get_precio_de_material(material=dm.material, ciudad=ciudad)
        if precio_de_material:
            total_materiales += float(precio_de_material.precio) * dm.coeficiente
        else:
            total_materiales += 0

    detalles_de_servicios = ServicioDeItem.objects.filter(item=item)
    for ds in detalles_de_servicios:
        precio_de_servicio = get_precio_de_servicio(servicio=ds.servicio, ciudad=ciudad)
        if precio_de_servicio:
            total_servicios += float(precio_de_servicio.precio) * ds.coeficiente
        else:
            total_servicios += 0
    return total_materiales + total_servicios


class MaterialDeItem(models.Model):
    class Meta:
        verbose_name = "Material de item"
        verbose_name_plural = "Materiales del item"

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    coeficiente = models.FloatField(default=1.0)


class ServicioDeItem(models.Model):
    class Meta:
        verbose_name = "Servicio de item"
        verbose_name_plural = "Servicios del item"

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    coeficiente = models.FloatField(default=1.0)

