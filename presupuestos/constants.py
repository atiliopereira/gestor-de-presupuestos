# -*- coding: utf-8 -*-


class EstadoPresupuestos:
    PENDIENTE = 'pen'
    PRESUPUESTADO = 'pre'
    ENVIADO = 'env'
    RECHAZADO = 'rec'
    APROBADO = 'apr'

    ESTADOS = (
        (PENDIENTE, 'Pendiente'),
        (PRESUPUESTADO, 'Presupuestado'),
        (ENVIADO, 'Enviado al cliente'),
        (RECHAZADO, 'Rechazado'),
        (APROBADO, 'Aprobado'),
    )
