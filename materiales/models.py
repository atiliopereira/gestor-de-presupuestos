import datetime
import os

import xlrd
from django.db import models

from sistema.models import Ciudad, get_ciudad_default


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
                                            on_delete=models.PROTECT, editable=False)

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


def get_default_cat_de_material():
    qs = CategoriaDeMaterial.objects.filter(nombre='Sin categoría')
    if qs.exists():
        return qs.first().pk
    else:
        return CategoriaDeMaterial.objects.create(nombre='Sin categoría').pk


class Material(models.Model):
    class Meta:
        verbose_name = "material"
        verbose_name_plural = "materiales"

    codigo = models.CharField(max_length=50, verbose_name="código")
    descripcion = models.CharField(max_length=150, verbose_name="descripción")
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.PROTECT)
    categoria = models.ForeignKey(CategoriaDeMaterial, on_delete=models.PROTECT, verbose_name="categoría",
                                  default=get_default_cat_de_material)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion} ({self.categoria.nombre})'


class PrecioDeMaterial(models.Model):
    class Meta:
        verbose_name_plural = "Precios de materiales"
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT, default=get_ciudad_default)
    precio = models.DecimalField(max_digits=15, decimal_places=0)
    inicio_de_vigencia = models.DateField(default=datetime.date.today)
    fin_de_vigencia = models.DateField(null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        super(PrecioDeMaterial, self).save(*args, **kwargs)
        registrar_fecha_de_fin_de_vigencia(material=self.material, ciudad=self.ciudad,
                                           inicio_de_vigencia=self.inicio_de_vigencia, self_pk=self.pk)


def registrar_fecha_de_fin_de_vigencia(material, ciudad, inicio_de_vigencia, self_pk):
    precios_anteriores = [precio for precio in
                          PrecioDeMaterial.objects.exclude(pk=self_pk).filter(material=material).filter(
                              ciudad=ciudad).order_by('-inicio_de_vigencia') if
                          not precio.fin_de_vigencia and precio.inicio_de_vigencia < inicio_de_vigencia]
    if precios_anteriores:
        precio_anterior = precios_anteriores[0]
        precio_anterior.fin_de_vigencia = inicio_de_vigencia - datetime.timedelta(days=1)
        precio_anterior.save()


def get_precio_de_material(**kwargs):
    material = kwargs.get("material")
    ciudad = kwargs.get("ciudad")

    if ciudad and material:
        fecha = kwargs.get("fecha") if 'fecha' in kwargs else datetime.date.today()
        precios = [precio for precio in
                   PrecioDeMaterial.objects.filter(material=material).filter(ciudad=ciudad).order_by(
                       '-inicio_de_vigencia') if not precio.fin_de_vigencia]
        if precios:
            for p in precios:
                if p.inicio_de_vigencia <= fecha:
                    return p
        else:
            #En caso de No encontrar precios registrado en la ciudad indicada, busca en todas las ciudades
            precios = [precio for precio in
                       PrecioDeMaterial.objects.filter(material=material).order_by(
                           '-inicio_de_vigencia') if not precio.fin_de_vigencia]
            if precios:
                for p in precios:
                    if p.inicio_de_vigencia <= fecha:
                        return p

    else:
        return None


def actualizar_precios_de_materiales(actualizacion_de_precios):
    extension = os.path.splitext(actualizacion_de_precios.archivo.path)[-1].lower()
    if extension == ".xls" or extension == ".xlsx":
        doc = actualizacion_de_precios.archivo.path
        try:
            wb = xlrd.open_workbook(doc)
            sheet = wb.sheet_by_index(0)
            sheet.cell_value(0, 0)
            actualizados = []
            no_existen = []
            for row in range(1, sheet.nrows):
                codigo = sheet.row_values(row)[0]
                descripcion = sheet.row_values(row)[1]
                precio = sheet.row_values(row)[2]
                ciudad = Ciudad.objects.get(pk=sheet.row_values(row)[4])
                unidad_de_medida = UnidadDeMedida.objects.get(pk=sheet.row_values(row)[5])
                inicio_de_vigencia = xlrd.xldate_as_datetime(sheet.row_values(row)[6], 0).date()

                material = Material.objects.filter(codigo=codigo).first()

                if material:
                    PrecioDeMaterial.objects.create(material=material, precio=precio,
                                                    ciudad=ciudad, inicio_de_vigencia=inicio_de_vigencia)
                    actualizados.append(material.codigo)
                else:
                    material = Material.objects.create(codigo=codigo, descripcion=descripcion,
                                                       unidad_de_medida=unidad_de_medida)
                    PrecioDeMaterial.objects.create(material=material, ciudad=ciudad, precio=precio,
                                                    inicio_de_vigencia=inicio_de_vigencia)
            return actualizados, no_existen
        except Exception as e:
            print(f'Error: {e}')
            return False


class ActualizacionDePreciosDeMateriales(models.Model):
    class Meta:
        verbose_name = "actualización de precios"
        verbose_name_plural = "actualizaciones de precios"
    fecha = models.DateField(default=datetime.date.today)
    archivo = models.FileField(upload_to='planillas_de_precios', null=True, blank=True)

    def save(self, *args, **kwargs):
        super(ActualizacionDePreciosDeMateriales, self).save(*args, **kwargs)
        actualizar_precios_de_materiales(self)
