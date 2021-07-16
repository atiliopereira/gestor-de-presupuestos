from django.shortcuts import render, redirect
from django.views.generic import DetailView

from cotizaciones.constants import EstadoDeSolicitud
from cotizaciones.models import Solicitud, MaterialDeSolicitud, ServicioDeSolicitud



class SolicitudDetailView(DetailView):
    model = Solicitud
    template_name = "admin/cotizaciones/solicitud/detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(SolicitudDetailView, self).get_context_data(**kwargs)
        context["materiales"] = MaterialDeSolicitud.objects.filter(solicitud=self.object)
        context["servicios"] = ServicioDeSolicitud.objects.filter(solicitud=self.object)
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
