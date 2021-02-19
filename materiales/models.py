import datetime

from django.db import models


class UnidadDeMedida(models.Model):
    class Meta:
        verbose_name = "unidad de medida"
        verbose_name_plural = "unidades de medida"

    nombre = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=10, verbose_name="Símbolo")

    def __str__(self):
        return f'{self.nombre} ({self.simbolo})'


class CategoriaDeMaterial(models.Model):
    class Meta:
        verbose_name = "categoría de materiales"
        verbose_name_plural = "categorías de materiales"

    nombre = models.CharField(max_length=200)
    categoria_padre = models.ForeignKey("self", related_name='categoria', verbose_name="Categoría", null=True,
                                        blank=True, on_delete=models.PROTECT)
    categoria_principal = models.ForeignKey("self", related_name='categoria_raiz',
                                            verbose_name="Categoría Principal", null=True, blank=True,
                                            on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.nombre_completo()}'

    def nombre_completo(self):
        return f'{self.categoria_padre.nombre_completo()} - {self.nombre}' if self.categoria_padre else f'{self.nombre}'

    def get_categoria_principal(self):
        categoria = self
        while categoria.categoria_padre:
            categoria = categoria.categoria_padre
        return categoria
    get_categoria_principal.short_description = "Categoría Principal"


class Material(models.Model):
    class Meta:
        verbose_name = "material"
        verbose_name_plural = "materiales"

    descripcion = models.CharField(max_length=150, verbose_name="descripción")
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.PROTECT)
    categoria = models.ForeignKey(CategoriaDeMaterial, on_delete=models.PROTECT, verbose_name="categoría")

    def __str__(self):
        return f'{self.descripcion}'


class PrecioDeMaterial(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=15, decimal_places=0)
    inicio_de_vigencia = models.DateField(default=datetime.date.today)
    fin_de_vigencia = models.DateField(blank=True, editable=False)


def get_precio_de_material(**kwargs):
    material = kwargs.get("material")
    if not material:
        return None
    else:
        fecha = kwargs.get("fecha") if 'fecha' in kwargs else datetime.date.today()
        precios = PrecioDeMaterial.objects.filter(material=material).order_by('-inicio_de_vigencia')
        for precio in precios:
            if precio.inicio_de_vigencia < fecha:
                return precio
