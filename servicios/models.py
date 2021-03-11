import datetime
import os

import xlrd
from django.db import models

from materiales.models import UnidadDeMedida
from sistema.models import Ciudad, get_ciudad_default


class CategoriaDeServicio(models.Model):
    class Meta:
        verbose_name = "categoría de servicios"
        verbose_name_plural = "categorías de servicios"

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


def get_default_cat_de_servicio():
    qs = CategoriaDeServicio.objects.filter(nombre='Sin categoría')
    if qs.exists():
        return qs.first().pk
    else:
        return CategoriaDeServicio.objects.create(nombre='Sin categoría').pk


class Servicio(models.Model):
    codigo = models.CharField(max_length=50, verbose_name="código")
    descripcion = models.CharField(max_length=150, verbose_name="descripción")
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.PROTECT)
    categoria = models.ForeignKey(CategoriaDeServicio, on_delete=models.PROTECT, verbose_name="categoría",
                                  default=get_default_cat_de_servicio)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion} ({self.categoria.nombre})'


class PrecioDeServicio(models.Model):
    class Meta:
        verbose_name_plural = "Precios de servicios"
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT, default=get_ciudad_default)
    precio = models.DecimalField(max_digits=15, decimal_places=0)
    inicio_de_vigencia = models.DateField(default=datetime.date.today)
    fin_de_vigencia = models.DateField(null=True, blank=True, editable=False)


def get_precio_de_servicio(**kwargs):
    servicio = kwargs.get("servicio")
    ciudad = kwargs.get("ciudad")
    if ciudad and servicio:
        fecha = kwargs.get("fecha") if 'fecha' in kwargs else datetime.date.today()
        precios = [precio for precio in
                   PrecioDeServicio.objects.filter(servicio=servicio).filter(ciudad=ciudad).order_by(
                       '-inicio_de_vigencia') if not precio.fin_de_vigencia]
        if precios:
            for p in precios:
                if p.inicio_de_vigencia <= fecha:
                    return p
        else:
            # En caso de No encontrar precios registrado en la ciudad indicada, busca en todas las ciudades
            precios = [precio for precio in
                       PrecioDeServicio.objects.filter(servicio=servicio).order_by(
                           '-inicio_de_vigencia') if not precio.fin_de_vigencia]
            if precios:
                for p in precios:
                    if p.inicio_de_vigencia <= fecha:
                        return p

    else:
        return None


def actualizar_precios_de_servicios(actualizacion_de_precios):
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
                servicio = Servicio.objects.filter(codigo=sheet.row_values(row)[0]).first()
                if servicio:
                    inicio_de_vigencia = xlrd.xldate_as_datetime(sheet.row_values(row)[4], 0).date()
                    PrecioDeServicio.objects.create(servicio=servicio, precio=sheet.row_values(row)[2],
                                                    inicio_de_vigencia=inicio_de_vigencia)
                    actualizados.append(servicio.codigo)
                else:
                    no_existen.append(sheet.row_values(row)[0])
            return actualizados, no_existen
        except Exception as e:
            print(f'Error: {e}')
            return False


class ActualizacionDePreciosDeServicios(models.Model):
    class Meta:
        verbose_name = "actualización de precios"
        verbose_name_plural = "actualizaciones de precios"
    fecha = models.DateField(default=datetime.date.today)
    archivo = models.FileField(upload_to='planillas_de_precios', null=True, blank=True)

    def save(self, *args, **kwargs):
        super(ActualizacionDePreciosDeServicios, self).save(*args, **kwargs)
        actualizar_precios_de_servicios(self)
