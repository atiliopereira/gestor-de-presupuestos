import datetime
import math
import random
from django.http import HttpResponse
from django.utils.text import get_valid_filename
import xlwt


# escritor xls
def listview_to_excel(values_list, name, titulos):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('Libro1')
    default_style = xlwt.Style.default_style
    estilo_cabecera = xlwt.easyxf('pattern: pattern solid, fore_colour black;'
                                  'font: colour white, bold True;')

    for col, datos in enumerate(titulos):
        sheet.write(0, col, datos, style=estilo_cabecera)

    for row, rowdata in enumerate(values_list):
        for col, val in enumerate(rowdata):
            style = default_style
            if "Total del item:" in rowdata:
                style = xlwt.easyxf("font: bold on; borders:  top_color black, top thin, bottom_color black, bottom thick; ")
            elif len(rowdata) == 3:
                style = xlwt.easyxf(
                    "font: bold on; borders: bottom_color black, bottom thick; ")
            elif "Subtotal" in rowdata:
                style = xlwt.easyxf("font: bold on; borders:  bottom_color black, bottom thin;")
            elif len(rowdata) == 2 and col == 0 or "Total:" in rowdata:
                style = xlwt.easyxf("font: bold on;")
            sheet.write(row + 1, col, val, style=style)
    response = HttpResponse(content_type='application/ms-excel')

    filename = "%s_%s.xls" % (name, datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
    filename = get_valid_filename(filename)
    response["Content-Disposition"] = "attachment; filename={0}".format(filename)
    book.save(response)
    return response


def separador_de_miles(numero, gs=False):
    numero = str(numero)
    vector = numero.split(".")
    s = vector[0]
    for i in range(len(vector[0]), 0, -3):
        if i == 1 and s[0] == "-":
            s = s[:i] + s[i:]
        else:
            s = s[:i] + "." + s[i:]
    a = s[:len(s) - 1]
    if gs:
        return a
    if len(vector) == 2 and vector[1] != "00":

        if len(vector[1]) > 2:
            dato = vector[1][0:2]
        else:
            dato = vector[1]
        a += "," + dato

    return a


def random_colors(size):
    result = []
    for i in range(size):
        linea = f'rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.5)'
        result.append(linea)
    return result


def mes_anho_en_letras(mes, anho):
    if mes == 1:
        return f'ENERO-{anho}'
    elif mes == 2:
        return f'FEBRERO-{anho}'
    elif mes == 3:
        return f'MARZO-{anho}'
    elif mes == 4:
        return f'ABRIL-{anho}'
    elif mes == 5:
        return f'MAYO-{anho}'
    elif mes == 6:
        return f'JUNIO-{anho}'
    elif mes == 7:
        return f'JULIO-{anho}'
    elif mes == 8:
        return f'AGOSTO-{anho}'
    elif mes == 9:
        return f'SETIEMBRE-{anho}'
    elif mes == 10:
        return f'OCTUBRE-{anho}'
    elif mes == 11:
        return f'NOVIEMBRE-{anho}'
    elif mes == 12:
        return f'DICIEMBRE-{anho}'
    else:
        return None


def texto_en_lineas(texto, longitud_renglon):
    resultado = []
    indice = iteracion = 0
    final = False
    if texto:
        while not final:
            linea = smart_truncate(
                texto[indice:len(texto)].replace('\r', '¶').replace('\n', '|'),
                longitud_renglon)
            indice += len(linea)
            resultado.append(linea.lstrip().lstrip('¶|'))
            iteracion += 1
            if not linea:
                final = True
    return resultado


def smart_truncate(content, length):
    index = content.find('¶|')
    if 0 < index < length:
        return content[:index]
    else:
        if len(content) <= length:
            return content
        else:
            return content[:length].rsplit(' ', 1)[0]


def separar(x):
    if type(x) not in [type(0), type(0)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + separar(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ".%03d%s" % (r, result)
    return "%d%s" % (x, result)


def numero_to_letras(numero):
    indicador = [("", ""), ("MIL", "MIL"), ("MILLON", "MILLONES"), ("MIL", "MIL"), ("BILLON", "BILLONES")]
    entero = int(numero)
    decimal = int(round((numero - entero) * 100))
    # print 'decimal : ',decimal
    contador = 0
    numero_letras = ""
    while entero > 0:
        a = entero % 1000
        if contador == 0:
            en_letras = convierte_cifra(a, 1).strip()
        else:
            en_letras = convierte_cifra(a, 0).strip()
        if a == 0:
            numero_letras = en_letras + " " + numero_letras
        elif a == 1:
            if contador in (1, 3):
                numero_letras = indicador[contador][0] + " " + numero_letras
            else:
                numero_letras = en_letras + " " + indicador[contador][0] + " " + numero_letras
        else:
            numero_letras = en_letras + " " + indicador[contador][1] + " " + numero_letras
        numero_letras = numero_letras.strip()
        contador = contador + 1
        entero = int(entero / 1000)
    numero_letras = numero_letras
    return numero_letras


def convierte_cifra(numero, sw):
    lista_centana = ["", ("CIEN", "CIENTO"), "DOSCIENTOS", "TRESCIENTOS", "CUATROCIENTOS", "QUINIENTOS", "SEISCIENTOS",
                     "SETECIENTOS", "OCHOCIENTOS", "NOVECIENTOS"]
    lista_decena = ["", (
        "DIEZ", "ONCE", "DOCE", "TRECE", "CATORCE", "QUINCE", "DIECISEIS", "DIECISIETE", "DIECIOCHO", "DIECINUEVE"),
                    ("VEINTE", "VEINTI"), ("TREINTA", "TREINTA Y "), ("CUARENTA", "CUARENTA Y "),
                    ("CINCUENTA", "CINCUENTA Y "), ("SESENTA", "SESENTA Y "),
                    ("SETENTA", "SETENTA Y "), ("OCHENTA", "OCHENTA Y "),
                    ("NOVENTA", "NOVENTA Y ")
                    ]
    lista_unidad = ["", ("UN", "UNO"), "DOS", "TRES", "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE"]
    centena = int(numero / 100)
    decena = int((numero - (centena * 100)) / 10)
    unidad = int(numero - (centena * 100 + decena * 10))
    # print "centena: ",centena, "decena: ",decena,'unidad: ',unidad

    texto_centena = ""
    texto_decena = ""
    texto_unidad = ""

    # Validad las centenas
    texto_centena = lista_centana[centena]
    if centena == 1:
        if (decena + unidad) != 0:
            texto_centena = texto_centena[1]
        else:
            texto_centena = texto_centena[0]

    # Valida las decenas
    texto_decena = lista_decena[decena]
    if decena == 1:
        texto_decena = texto_decena[unidad]
    elif decena > 1:
        if unidad != 0:
            texto_decena = texto_decena[1]
        else:
            texto_decena = texto_decena[0]
    # Validar las unidades
    # print "texto_unidad: ",texto_unidad
    if decena != 1:
        texto_unidad = lista_unidad[unidad]
        if unidad == 1:
            texto_unidad = texto_unidad[sw]

    return "%s %s %s" % (texto_centena, texto_decena, texto_unidad)


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper