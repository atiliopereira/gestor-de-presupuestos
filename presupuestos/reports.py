# -*- coding: utf-8 -*-
from items.models import DetalleDeItem
from presupuestos.models import Presupuesto, DetalleDePresupuesto
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
        for di in DetalleDeItem.objects.filter(item=dp.item).distinct('material'):
            cantidad_total = float(dp.cantidad) * di.coeficiente
            total_material = float(di.material.precio_actual()) * cantidad_total
            lista_datos.append([
                di.material.descripcion,
                cantidad_total,
                di.material.unidad_de_medida.simbolo,
                di.material.precio_actual(),
                total_material
            ])
        lista_datos.append(["", "", "", "Total del item:", dp.subtotal])
        lista_datos.append([])
    lista_datos.append(["", "", "", "Total:", separar(int(presupuesto.total))])
    response = listview_to_excel(lista_datos, nombre_archivo, titulos)
    return response