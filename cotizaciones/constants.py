# -*- coding: utf-8 -*-


class TiposDeCotizacion:
    MATERIAL = 'M'
    SERVICIOS = 'S'

    TIPOS = (
        (MATERIAL, 'Materiales'),
        (SERVICIOS, 'Mano de obra'),
    )


class EstadoDeSolicitud:
    VIGENTE = 'vi'
    CONCRETADO = 'co'
    CANCELADO = 'ca'

    ESTADOS = (
        (VIGENTE, 'Vigente'),
        (CONCRETADO, 'Concretado'),
        (CANCELADO, 'Cancelado')
    )
