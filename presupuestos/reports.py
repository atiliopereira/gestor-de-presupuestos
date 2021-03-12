# -*- coding: utf-8 -*-
from items.models import MaterialDeItem, ServicioDeItem
from materiales.models import get_precio_de_material, Material
from presupuestos.models import Presupuesto, DetalleDePresupuesto
from servicios.models import get_precio_de_servicio, Servicio
from tillner.globales import listview_to_excel, separar


def presupuesto_report(request, id):
    presupuesto = Presupuesto.objects.get(pk=id)
    nombre_archivo = f'{presupuesto.numero_de_presupuesto}'
    titulos = []

    lista_datos = [["Presupuesto Nº:", presupuesto.numero_de_presupuesto],
                   ["Fecha:", presupuesto.fecha.strftime("%d/%m/%Y")],
                   ["Cliente:", presupuesto.cliente.nombre],
                   ["Obra:", presupuesto.obra]]
    if presupuesto.direccion:
        lista_datos.append(["Dirección:", presupuesto.direccion])
    if presupuesto.ciudad:
        lista_datos.append(["Ciudad:", presupuesto.ciudad.nombre])
    lista_datos.append([])

    for dp in DetalleDePresupuesto.objects.filter(presupuesto=presupuesto):
        lista_datos.append([
            dp.item.descripcion,
            dp.cantidad,
            dp.item.unidad_de_medida.simbolo,
        ])
        lista_datos.append(["MAT/MDO", "Cantidad", "Unidad", "Precio Unit.", "Subtotal"])
        for mi in MaterialDeItem.objects.filter(item=dp.item).distinct('material'):
            cantidad_total = float(dp.cantidad) * mi.coeficiente
            precio_de_material = get_precio_de_material(material=mi.material, ciudad=presupuesto.ciudad,
                                                        fecha=presupuesto.fecha)
            total_material = float(precio_de_material.precio) * cantidad_total
            lista_datos.append([
                mi.material.descripcion,
                cantidad_total,
                mi.material.unidad_de_medida.simbolo,
                precio_de_material.precio,
                total_material
            ])
        for si in ServicioDeItem.objects.filter(item=dp.item).distinct('servicio'):
            cantidad_total = float(dp.cantidad) * si.coeficiente
            precio_de_servicio = get_precio_de_servicio(servicio=si.servicio, ciudad=presupuesto.ciudad,
                                                        fecha=presupuesto.fecha)
            total_servicio = float(precio_de_servicio.precio) * cantidad_total
            lista_datos.append([
                si.servicio.descripcion,
                cantidad_total,
                si.servicio.unidad_de_medida.simbolo,
                precio_de_servicio.precio,
                total_servicio
            ])
        lista_datos.append(["", "", "", "Total del item:", dp.subtotal])
        lista_datos.append([])
    lista_datos.append(["", "", "", "Total:", separar(int(presupuesto.total))])
    response = listview_to_excel(lista_datos, nombre_archivo, titulos)
    return response


def presupuesto_materiales_report(request, id):
    presupuesto = Presupuesto.objects.get(pk=id)
    materiales = [item for item in presupuesto.get_lista_de_recursos().items() if item[0][0] == 'm']
    lista_datos = []

    for item in materiales:
        material_pk = int(item[0][1:])
        m = Material.objects.get(pk=material_pk)
        lista_datos.append([
            m.descripcion,
            item[1],
            m.unidad_de_medida.simbolo,
            ''
        ])
    lista_datos.append([''])
    lista_datos.append(["Fecha:", presupuesto.fecha.strftime("%d/%m/%Y"), "Ciudad:", presupuesto.ciudad.nombre])
    nombre_archivo = f'materiales_{presupuesto.numero_de_presupuesto}'
    titulos = ['Material', 'Cantidad Requerida', 'Unidad', 'Precio']
    response = listview_to_excel(lista_datos, nombre_archivo, titulos)
    return response


def presupuesto_servicios_report(request, id):
    presupuesto = Presupuesto.objects.get(pk=id)
    servicios = [item for item in presupuesto.get_lista_de_recursos().items() if item[0][0] == 's']
    lista_datos = []

    for item in servicios:
        servicio_pk = int(item[0][1:])
        s = Servicio.objects.get(pk=servicio_pk)
        lista_datos.append([
            s.descripcion,
            item[1],
            s.unidad_de_medida.simbolo,
            ''
        ])
    lista_datos.append([''])
    lista_datos.append(["Fecha:", presupuesto.fecha.strftime("%d/%m/%Y"), "Ciudad:", presupuesto.ciudad.nombre])
    nombre_archivo = f'mano_de_obra_{presupuesto.numero_de_presupuesto}'
    titulos = ['Servicio', 'Cantidad Requerida', 'Unidad', 'Precio']
    response = listview_to_excel(lista_datos, nombre_archivo, titulos)
    return response
