# -*- coding: utf-8 -*-
import os
from io import BytesIO

from django.http import HttpResponse
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from items.models import MaterialDeItem, ServicioDeItem
from materiales.models import get_precio_de_material, Material
from presupuestos.models import Presupuesto, DetalleDePresupuesto, AdicionalDePresupuesto
from servicios.models import get_precio_de_servicio, Servicio
from sistema.models import Usuario
from tillner.globales import listview_to_excel, separar, truncate, number_to_right


def presupuesto_excel(request, id):
    presupuesto = Presupuesto.objects.get(pk=id)
    factor_de_margen = float(1 + presupuesto.margen_de_ganancia/100)
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
            dp.item.unidad_de_medida.simbolo.lower(),
        ])
        lista_datos.append(["MAT/MDO", "Cantidad", "Unidad", "Precio Unit.", "Subtotal"])
        for mi in MaterialDeItem.objects.filter(item=dp.item).distinct('material'):
            cantidad_total = float(dp.cantidad) * mi.coeficiente
            precio_de_material = get_precio_de_material(material=mi.material, ciudad=presupuesto.ciudad,
                                                        fecha=presupuesto.fecha)
            total_material = float(precio_de_material.precio) * cantidad_total * factor_de_margen
            lista_datos.append([
                mi.material.__str__(),
                cantidad_total,
                mi.material.unidad_de_medida.simbolo.lower(),
                float(precio_de_material.precio) * factor_de_margen,
                total_material
            ])
        for si in ServicioDeItem.objects.filter(item=dp.item).distinct('servicio'):
            cantidad_total = float(dp.cantidad) * si.coeficiente
            precio_de_servicio = get_precio_de_servicio(servicio=si.servicio, ciudad=presupuesto.ciudad,
                                                        fecha=presupuesto.fecha)
            total_servicio = float(precio_de_servicio.precio) * cantidad_total * factor_de_margen
            lista_datos.append([
                si.servicio.__str__(),
                cantidad_total,
                si.servicio.unidad_de_medida.simbolo.lower(),
                float(precio_de_servicio.precio) * factor_de_margen,
                total_servicio
            ])
        lista_datos.append(["", "", "", "Total del item:", dp.subtotal])
        lista_datos.append([])
    for ap in AdicionalDePresupuesto.objects.filter(presupuesto=presupuesto):
        lista_datos.append([
            ap.descripcion,
            ap.cantidad,
            ap.unidad_de_medida.simbolo.lower(),
        ])
        lista_datos.append(["", "", "", "Total del item:", ap.subtotal])
        lista_datos.append([])
    lista_datos.append(["", "", "", "Total:", separar(int(presupuesto.total))])
    response = listview_to_excel(lista_datos, nombre_archivo, titulos)
    return response


def presupuesto_pdf(request, id):
    def contenido(canvas, presupuesto):
        usuario = Usuario.objects.get(pk=presupuesto.cliente.creado_por.pk)
        if usuario.logo:
            rp = os.path.join(os.path.dirname(os.path.abspath(__file__)), usuario.logo.path)
            canvas.drawInlineImage(rp, 460, 725, width=inch * 1.3, height=inch * 1.3)
        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawString(190, 790, f'Presupuesto Nº{presupuesto.numero_de_presupuesto}')
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(30, 770, 'Fecha:')
        canvas.drawString(30, 755, 'Cliente:')
        canvas.drawString(30, 740, 'Obra:')
        canvas.drawString(30, 725, 'Ciudad:')
        canvas.drawString(30, 710, 'Validez:')
        canvas.drawString(30, 695, 'Obs:')
        canvas.setFont("Helvetica", 12)
        canvas.drawString(100, 770, f'{presupuesto.fecha.strftime("%d/%m/%Y")}')
        canvas.drawString(100, 755, f'{presupuesto.cliente.nombre}')
        canvas.drawString(100, 740, f'{presupuesto.obra}')
        canvas.drawString(100, 725, f'{presupuesto.ciudad.nombre}')
        canvas.drawString(100, 710, f'{presupuesto.validez_del_presupuesto} días')
        observaciones = f'-'
        if presupuesto.observaciones:
            observaciones = presupuesto.observaciones
        canvas.drawString(100, 695, f'{observaciones}')

        row = 680
        for dp in DetalleDePresupuesto.objects.filter(presupuesto=presupuesto):
            row -= 20
            canvas.setFont("Helvetica-Bold", 12)
            canvas.drawString(30, row, f'{dp.item.descripcion}: {dp.cantidad} {dp.item.unidad_de_medida.simbolo.lower()}')

            canvas.setLineWidth(1)
            canvas.line(30, row-2, 570, row-2)
            row -= 15
            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(30, row, f'MAT/MDO')
            canvas.drawString(343, row, f'Cantidad')
            canvas.drawString(403, row, f'Unidad')
            canvas.drawString(452, row, f'Precio Unit.')
            canvas.drawString(526, row, f'Subtotal')
            row -= 15
            for mi in MaterialDeItem.objects.filter(item=dp.item).distinct('material'):
                cantidad_total = float(dp.cantidad) * mi.coeficiente
                precio_de_material = get_precio_de_material(material=mi.material, ciudad=presupuesto.ciudad,
                                                            fecha=presupuesto.fecha)
                total_material = float(precio_de_material.precio) * cantidad_total * factor_de_margen

                # Cantidades numéricas en letras
                cant = f'{truncate(cantidad_total, 2)}'
                pu = f'{number_to_right(separar(int(float(precio_de_material.precio) * factor_de_margen)))}'
                st = f'{number_to_right(separar(int(total_material)))}'

                canvas.setFont("Helvetica", 9)
                descripcion = f'{mi.material.descripcion}'
                canvas.drawString(30, row, (descripcion[:73] + '..') if len(descripcion) > 73 else descripcion)

                canvas.drawString(418, row, f'{mi.material.unidad_de_medida.simbolo.lower()}')

                # Posiciones en x calculadas según longitud de string
                x_cant = 390 - stringWidth(cant, "Helvetica", 9)
                x_pu = 513 - stringWidth(pu, "Helvetica", 9)
                x_st = 570 - stringWidth(st, "Helvetica", 9)

                canvas.drawString(x_cant, row, cant)
                canvas.drawString(x_pu, row, pu)
                canvas.drawString(x_st, row, st)
                row -= 15

            for si in ServicioDeItem.objects.filter(item=dp.item).distinct('servicio'):
                cantidad_total = float(dp.cantidad) * si.coeficiente
                precio_de_servicio = get_precio_de_servicio(servicio=si.servicio, ciudad=presupuesto.ciudad,
                                                            fecha=presupuesto.fecha)
                total_servicio = float(precio_de_servicio.precio) * cantidad_total * factor_de_margen

                # Precios en letras
                cant = f'{truncate(cantidad_total, 2)}'
                pu = f'{number_to_right(separar(int(float(precio_de_servicio.precio) * factor_de_margen)))}'
                st = f'{number_to_right(separar(int(total_servicio)))}'

                canvas.setFont("Helvetica", 9)
                descripcion = f'{si.servicio.descripcion}'
                canvas.drawString(30, row, (descripcion[:73] + '..') if len(descripcion) > 73 else descripcion)

                canvas.drawString(418, row, f'{si.servicio.unidad_de_medida.simbolo.lower()}')

                # Posiciones en x calculadas según longitud de string
                x_cant = 390 - stringWidth(cant, "Helvetica", 9)
                x_pu = 513 - stringWidth(pu, "Helvetica", 9)
                x_st = 570 - stringWidth(st, "Helvetica", 9)

                canvas.drawString(x_cant, row, cant)
                canvas.drawString(x_pu, row, pu)
                canvas.drawString(x_st, row, st)
                row -= 15

            canvas.line(30, row + 12, 570, row + 12)
            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(400, row, f'Precio Item:')
            canvas.setFont("Helvetica", 11)
            precio_item = f'{number_to_right(separar(int(float(dp.subtotal) * factor_de_margen)))}'
            px = 570 - stringWidth(precio_item, "Helvetica", 11)
            canvas.drawString(px, row, precio_item)

        for ap in AdicionalDePresupuesto.objects.filter(presupuesto=presupuesto):
            row -= 20
            canvas.setFont("Helvetica-Bold", 12)
            canvas.drawString(30, row,
                              f'{ap.descripcion}: {ap.cantidad} {ap.unidad_de_medida.simbolo.lower()}')

            row -= 15
            canvas.setLineWidth(1)
            canvas.line(30, row + 12, 570, row + 12)
            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(400, row, f'Precio Item:')
            canvas.setFont("Helvetica", 11)
            precio_item = f'{number_to_right(separar(int(float(ap.subtotal) * factor_de_margen)))}'
            px = 570 - stringWidth(precio_item, "Helvetica", 11)
            canvas.drawString(px, row, precio_item)

        row -= 15
        canvas.line(30, row - 10, 570, row - 10)
        canvas.line(30, row - 12, 570, row - 12)
        row -= 25
        canvas.setFont("Helvetica-Bold", 12)
        precio_total = f'{number_to_right(separar(int(float(presupuesto.total) * factor_de_margen)))}'
        px = 570 - stringWidth(precio_total, "Helvetica-Bold", 12)
        canvas.drawString(400, row, f'Total:')
        canvas.drawString(px, row, precio_total)

        canvas.setFont("Helvetica", 8)
        # 396 para justificar a la derecha
        canvas.drawString(30, 10, f'Presupuesto creado en construyaenlinea.com.py')

    presupuesto = Presupuesto.objects.get(pk=id)
    factor_de_margen = float(1 + presupuesto.margen_de_ganancia / 100)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="presupuesto_report.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    contenido(p, presupuesto)
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def presupuesto_materiales_report(request, id):
    presupuesto = Presupuesto.objects.get(pk=id)
    materiales = [item for item in presupuesto.get_lista_de_recursos().items() if item[0][0] == 'm']
    lista_datos = []

    for item in materiales:
        # La estructura del item es: ('m1', 2.0)

        material_pk = int(item[0][1:])
        m = Material.objects.get(pk=material_pk)
        precio_de_material = get_precio_de_material(material=m, ciudad=presupuesto.ciudad,
                                                    fecha=presupuesto.fecha)
        total_material = float(precio_de_material.precio) * item[1]
        lista_datos.append([
            m.__str__(),
            item[1],
            m.unidad_de_medida.simbolo.lower(),
            precio_de_material.precio,
            total_material
        ])
    lista_datos.append([''])
    lista_datos.append(["Fecha:", presupuesto.fecha.strftime("%d/%m/%Y"), "Ciudad:", presupuesto.ciudad.nombre])
    nombre_archivo = f'materiales_{presupuesto.numero_de_presupuesto}'
    titulos = ['Material', 'Cantidad Requerida', 'Unidad', 'Precio Unit', 'Subtotal']
    response = listview_to_excel(lista_datos, nombre_archivo, titulos)
    return response


def presupuesto_servicios_report(request, id):
    presupuesto = Presupuesto.objects.get(pk=id)
    servicios = [item for item in presupuesto.get_lista_de_recursos().items() if item[0][0] == 's']
    lista_datos = []

    for item in servicios:
        # La estructura del item es: ('m1', 2.0)

        servicio_pk = int(item[0][1:])
        s = Servicio.objects.get(pk=servicio_pk)
        precio_de_servicio = get_precio_de_servicio(servicio=s, ciudad=presupuesto.ciudad,
                                                    fecha=presupuesto.fecha)
        total_servicio = float(precio_de_servicio.precio) * item[1]
        lista_datos.append([
            s.__str__(),
            item[1],
            s.unidad_de_medida.simbolo.lower(),
            precio_de_servicio.precio,
            total_servicio
        ])
    lista_datos.append([''])
    lista_datos.append(["Fecha:", presupuesto.fecha.strftime("%d/%m/%Y"), "Ciudad:", presupuesto.ciudad.nombre])
    nombre_archivo = f'mano_de_obra_{presupuesto.numero_de_presupuesto}'
    titulos = ['Servicio', 'Cantidad Requerida', 'Unidad', 'Precio Unit', 'Subtotal']
    response = listview_to_excel(lista_datos, nombre_archivo, titulos)
    return response
