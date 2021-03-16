# -*- coding: utf-8 -*-
import os
from io import BytesIO

from django.http import HttpResponse
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from items.models import MaterialDeItem, ServicioDeItem
from materiales.models import get_precio_de_material, Material
from presupuestos.models import Presupuesto, DetalleDePresupuesto
from servicios.models import get_precio_de_servicio, Servicio
from sistema.models import Usuario
from tillner.globales import listview_to_excel, separar


def presupuesto_excel(request, id):
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


def presupuesto_pdf(request, id):
    def contenido(canvas, presupuesto):
        usuario = Usuario.objects.get(pk=presupuesto.cliente.creado_por.pk)
        rp = os.path.join(os.path.dirname(os.path.abspath(__file__)), usuario.logo.path)
        canvas.drawInlineImage(rp, 460, 725, width=inch * 1.3, height=inch * 1.3)
        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawString(190, 790, f'Presupuesto Nº{presupuesto.numero_de_presupuesto}')
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(30, 770, 'Fecha:')
        canvas.drawString(30, 755, 'Cliente:')
        canvas.drawString(30, 740, 'Obra:')
        canvas.drawString(30, 725, 'Ciudad:')
        canvas.setFont("Helvetica", 12)
        canvas.drawString(100, 770, f'{presupuesto.fecha.strftime("%d/%m/%Y")}')
        canvas.drawString(100, 755, f'{presupuesto.cliente.nombre}')
        canvas.drawString(100, 740, f'{presupuesto.obra}')
        canvas.drawString(100, 725, f'{presupuesto.ciudad.nombre}')

        row = 705
        for dp in DetalleDePresupuesto.objects.filter(presupuesto=presupuesto):
            row -= 20
            canvas.setFont("Helvetica-Bold", 12)
            canvas.drawString(30, row, f'{dp.item.descripcion}: {dp.cantidad} {dp.item.unidad_de_medida.simbolo}')

            canvas.setLineWidth(1)
            canvas.line(30, row-2, 570, row-2)
            row -= 15
            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(30, row, f'MAT/MDO')
            canvas.drawString(180, row, f'Cantidad')
            canvas.drawString(250, row, f'Unidad')
            canvas.drawString(350, row, f'Precio Unitario')
            canvas.drawString(480, row, f'Subtotal')
            row -= 15
            for mi in MaterialDeItem.objects.filter(item=dp.item).distinct('material'):
                cantidad_total = float(dp.cantidad) * mi.coeficiente
                precio_de_material = get_precio_de_material(material=mi.material, ciudad=presupuesto.ciudad,
                                                            fecha=presupuesto.fecha)
                total_material = float(precio_de_material.precio) * cantidad_total

                canvas.setFont("Helvetica", 11)
                canvas.drawString(30, row, f'{mi.material.descripcion}')
                canvas.drawString(200, row, f'{cantidad_total}')
                canvas.drawString(250, row, f'{mi.material.unidad_de_medida.simbolo}')
                canvas.drawString(350, row, f'{separar(int(precio_de_material.precio))}')
                canvas.drawString(480, row, f'{separar(int(total_material))}')
                row -= 15

            for si in ServicioDeItem.objects.filter(item=dp.item).distinct('servicio'):
                cantidad_total = float(dp.cantidad) * si.coeficiente
                precio_de_servicio = get_precio_de_servicio(servicio=si.servicio, ciudad=presupuesto.ciudad,
                                                            fecha=presupuesto.fecha)
                total_servicio = float(precio_de_servicio.precio) * cantidad_total
                canvas.setFont("Helvetica", 11)
                canvas.drawString(30, row, f'{si.servicio.descripcion}')
                canvas.drawString(200, row, f'{cantidad_total}')
                canvas.drawString(250, row, f'{si.servicio.unidad_de_medida.simbolo}')
                canvas.drawString(350, row, f'{separar(int(precio_de_servicio.precio))}')
                canvas.drawString(480, row, f'{separar(int(total_servicio))}')
                row -= 15

            canvas.line(30, row + 12, 570, row + 12)
            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(400, row, f'Precio Item:')
            canvas.setFont("Helvetica", 11)
            canvas.drawString(480, row, f'{separar(int(dp.subtotal))}')
        row -= 25
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(400, row, f'Total:')
        canvas.drawString(480, row, f'{separar(int(presupuesto.total))}')




    presupuesto = Presupuesto.objects.get(pk=id)
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
