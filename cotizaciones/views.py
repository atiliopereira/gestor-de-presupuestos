import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from cotizaciones.constants import TiposDeCotizacion
from cotizaciones.forms import SolicitudDeCotizacionForm
from cotizaciones.models import Solicitud, DetalleDeSolicitud
from materiales.models import Material
from presupuestos.models import Presupuesto, DetalleDePresupuesto
from servicios.models import Servicio


class SolicitudDetailView(DetailView):
    model = Solicitud
    template_name = "admin/cotizaciones/solicitud/detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(SolicitudDetailView, self).get_context_data(**kwargs)
        filtro = 'm' if self.object.tipo == TiposDeCotizacion.MATERIAL else 's'
        items = [item for item in self.object.presupuesto.get_lista_de_recursos().items() if
                               item[0][0] == filtro]
        detalles = []
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
        return context


def crear_solicitud(request, pk, tipo):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    detalles_en_presupuesto = DetalleDePresupuesto.objects.filter(presupuesto=presupuesto)

    if request.method == 'POST':
        form = SolicitudDeCotizacionForm(request.POST)
        if form.is_valid():
            tipo_de_cotizacion = TiposDeCotizacion.MATERIAL
            if 2 == int(tipo):
                tipo_de_cotizacion = TiposDeCotizacion.SERVICIOS
            solicitud = Solicitud.objects.create(fecha=datetime.date.today(), presupuesto=presupuesto,
                                                 tipo=tipo_de_cotizacion)
            solicitud.comentarios = form.cleaned_data['comentarios']
            solicitud.vencimiento = form.cleaned_data['vencimiento']
            solicitud.save()
            for dp in detalles_en_presupuesto:
                # Materiales: tipo 1, Servicios: tipo 2.
                if tipo == 1:
                    #comprobación de que existen materiales en el item
                    if dp.get_recursos_de_detalle()[0]:
                        DetalleDeSolicitud.objects.create(solicitud=solicitud, detalle_de_presupuesto=dp)
                elif tipo == 2:
                    #comprobación de que existen servicios en el item
                    if dp.get_recursos_de_detalle()[1]:
                        DetalleDeSolicitud.objects.create(solicitud=solicitud, detalle_de_presupuesto=dp)

            url = f'/admin/cotizaciones/solicitud_detail/{solicitud.pk}'
            return HttpResponseRedirect(url)

    else:
        form = SolicitudDeCotizacionForm(initial={'comentarios': '', })
    extra_context = {}
    extra_context.update({
        'form': form,
        'presupuesto': presupuesto,
        'detalles': detalles_en_presupuesto,
        'tipo': tipo,
        'app_label': u'presupuestos',
    })
    return render(request, 'admin/cotizaciones/solicitud/solicitud_de_cotizacion.html', extra_context)


def get_solicitudes_queryset(request, form):
    qs = Solicitud.objects.all()
    if form.cleaned_data.get('tipo', ''):
        qs = qs.filter(tipo=form.cleaned_data['tipo'])
    if form.cleaned_data.get('ciudad', ''):
        qs = qs.filter(presupuesto__ciudad=form.cleaned_data.get('ciudad', ''))
    if form.cleaned_data.get('desde', ''):
        qs = qs.filter(vencimiento__gte=form.cleaned_data.get('desde', ''))
    if form.cleaned_data.get('hasta', ''):
        qs = qs.filter(vencimiento__lte=form.cleaned_data.get('hasta', ''))

    return qs
