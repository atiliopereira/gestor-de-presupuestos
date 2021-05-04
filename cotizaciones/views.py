from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView

from cotizaciones.constants import TiposDeCotizacion, EstadoDeSolicitud
from cotizaciones.models import Solicitud, Cotizacion, MaterialDeCotizacion, ServicioDeCotizacion
from materiales.models import Material
from servicios.models import Servicio


class CotizacionesDashboardView(TemplateView):
    template_name = 'cotizaciones_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(CotizacionesDashboardView, self).get_context_data(**kwargs)
        context["total_solicitudes"] = Solicitud.objects.all().count()
        context["total_cotizaciones"] = Cotizacion.objects.filter(creado_por=self.request.user).count()
        return context


class SolicitudDetailView(DetailView):
    model = Solicitud
    template_name = "admin/cotizaciones/solicitud/detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(SolicitudDetailView, self).get_context_data(**kwargs)

        # Obtencion de los materiales o servicios del presupuesto
        filtro = 'm' if self.object.tipo == TiposDeCotizacion.MATERIAL else 's'
        items = [item for item in self.object.presupuesto.get_lista_de_recursos().items() if
                               item[0][0] == filtro]
        detalles = []
        # Cada item es una tupla de la forma (m13, 2.0)

        for item in items:
            if filtro == 'm':
                material_pk = int(item[0][1:])
                m = Material.objects.get(pk=material_pk)
                detalles.append([
                    m,
                    item[1],
                ])
            else:
                servicio_pk = int(item[0][1:])
                s = Servicio.objects.get(pk=servicio_pk)
                detalles.append([
                    s,
                    item[1],
                ])
        context["detalles"] = detalles
        context["cotizaciones"] = Cotizacion.objects.filter(solicitud=self.object)
        return context


def cancelar_solicitud(request, pk):
    solicitud = Solicitud.objects.get(pk=pk)
    if request.method == 'POST':
        solicitud.estado = EstadoDeSolicitud.CANCELADO
        solicitud.save()

        return redirect('/admin/cotizaciones/solicitud/')

    mensaje = f'¿Confirmar cancelación de la {solicitud}?'
    advertencia = f'ADVERTENCIA: esta acción no se puede revertir.'
    return render(request,
                  'admin/cotizaciones/solicitud/solicitud_confirm.html',
                  {'mensaje': mensaje, 'advertencia': advertencia})


def concretar_solicitud(request, pk):
    solicitud = Solicitud.objects.get(pk=pk)
    if request.method == 'POST':
        solicitud.estado = EstadoDeSolicitud.CONCRETADO
        solicitud.save()

        return redirect('/admin/cotizaciones/solicitud/')

    mensaje = f'¿Confirmar como concretada la {solicitud}?'
    advertencia = f'ADVERTENCIA: esta acción no se puede revertir.'
    return render(request,
                  'admin/cotizaciones/solicitud/solicitud_confirm.html',
                  {'mensaje': mensaje, 'advertencia': advertencia})


def get_solicitudes_queryset(request, form):
    qs = Solicitud.objects.all()
    if form.cleaned_data.get('tipo', ''):
        qs = qs.filter(tipo=form.cleaned_data['tipo'])
    if form.cleaned_data.get('estado', ''):
        qs = qs.filter(tipo=form.cleaned_data['estado'])
    if form.cleaned_data.get('ciudad', ''):
        qs = qs.filter(presupuesto__ciudad=form.cleaned_data.get('ciudad', ''))
    if form.cleaned_data.get('desde', ''):
        qs = qs.filter(vencimiento__gte=form.cleaned_data.get('desde', ''))
    if form.cleaned_data.get('hasta', ''):
        qs = qs.filter(vencimiento__lte=form.cleaned_data.get('hasta', ''))

    return qs


class CotizacionDetailView(DetailView):
    model = Cotizacion
    template_name = "admin/cotizaciones/cotizacion/detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(CotizacionDetailView, self).get_context_data(**kwargs)
        context["materiales"] = MaterialDeCotizacion.objects.filter(cotizacion=self.object)
        context["servicios"] = ServicioDeCotizacion.objects.filter(cotizacion=self.object)
        return context
