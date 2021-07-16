from django.db import models
from materiales.models import UnidadDeMedida, Material, get_precio_de_material
from servicios.models import Servicio, get_precio_de_servicio
from sistema.models import Ciudad


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

    def ciudad_sin_precio(self):
        for ciudad in Ciudad.objects.all():
            if not get_precio_unitario_de_item(self, ciudad):
                return f'Error de precio en {ciudad.nombre}'


def get_precio_unitario_de_item(item, ciudad):
    '''
    :param item: item requerido, contiene materiales, servicios y un coeficiente de ponderación para cada uno.
    :param ciudad: utilizada para obtener precio, ya que varía según la ciudad (tanto materiales como servicios)
    :return: Suma de precio de materiales y servicios requeridos para elaborar el item.
    El return None sirve para detectar materiales que no tengan cargado ningún precio, ya que la función
    'get_precio_de_material/servicio' ya contempla el caso de que no se encuentre precio para la ciudad solicitada
    '''
    total_materiales = total_servicios = 0

    detalles_de_materiales = MaterialDeItem.objects.filter(item=item)
    for dm in detalles_de_materiales:
        precio_de_material = get_precio_de_material(material=dm.material, ciudad=ciudad)
        if precio_de_material:
            total_materiales += float(precio_de_material.precio) * dm.coeficiente
        else:
            return None

    detalles_de_servicios = ServicioDeItem.objects.filter(item=item)
    for ds in detalles_de_servicios:
        precio_de_servicio = get_precio_de_servicio(servicio=ds.servicio, ciudad=ciudad)
        if precio_de_servicio:
            total_servicios += float(precio_de_servicio.precio) * ds.coeficiente
        else:
            return None #Esto es para detectar servicios que no tengan cargado ningún precio
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

