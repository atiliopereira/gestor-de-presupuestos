# -*- coding: utf-8 -*-
from django.test import TestCase

from materiales.models import UnidadDeMedida, CategoriaDeMaterial, Material


class UnidadDeMedidaTest(TestCase):

    def crear_unidad_de_medida(self, nombre="hora/hombre", simbolo="hr/h"):
        return UnidadDeMedida.objects.create(nombre=nombre, simbolo=simbolo)

    def test_unidad_de_medida_creacion(self):
        udm = self.crear_unidad_de_medida()
        self.assertTrue(isinstance(udm, UnidadDeMedida))
        self.assertEqual(udm.__str__(), f'{udm.nombre} ({udm.simbolo})')


class CategoriaDeMaterialTest(TestCase):

    def crear_categoria_de_material(self, nombre="Reparación de cañerías"):
        return CategoriaDeMaterial.objects.create(nombre=nombre)

    def test_categoria_de_material_creacion(self):
        cdm = self.crear_categoria_de_material()
        self.assertTrue(isinstance(cdm, CategoriaDeMaterial))
        self.assertEqual(cdm.__str__(), f'{cdm.nombre_completo()}')


class MaterialTest(TestCase):

    def crear_material(self, descripcion='caño de 5"'):
        udm = UnidadDeMedida.objects.create(nombre="hora/hombre", simbolo="hr/h")
        categoria = CategoriaDeMaterial.objects.create(nombre="Reparación de cañerías")
        return Material.objects.create(descripcion=descripcion, unidad_de_medida=udm, categoria=categoria)

    def test_material_creacion(self):
        m = self.crear_material()
        self.assertTrue(isinstance(m, Material))
        self.assertEqual(m.__str__(), f'{m.descripcion}')
