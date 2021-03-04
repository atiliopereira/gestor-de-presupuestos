# -*- coding: utf-8 -*-


class EstadoPresupuestos:
    PENDIENTE = 'pen'
    ENVIADO = 'env'
    RECHAZADO = 'rec'
    APROBADO = 'apr'

    ESTADOS = (
        (PENDIENTE, 'Pendiente'),
        (ENVIADO, 'Enviado al cliente'),
        (RECHAZADO, 'Rechazado'),
        (APROBADO, 'Aprobado'),
    )
