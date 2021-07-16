from django.views.generic import DetailView, TemplateView
from django.shortcuts import render, redirect

from clientes.models import Cliente
from items.models import Item
from materiales.models import Material, ActualizacionDePreciosDeMateriales
from presupuestos.models import Presupuesto, DetalleDePresupuesto, AdicionalDePresupuesto
from presupuestos.constants import EstadoPresupuestos
from servicios.models import ActualizacionDePreciosDeServicios, Servicio


class PresupuestoDashboardView(TemplateView):
    template_name = 'presupuesto_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(PresupuestoDashboardView, self).get_context_data(**kwargs)
        context["total_presupuestos"] = Presupuesto.objects.filter(cliente__creado_por=self.request.user).count()
        context["total_clientes"] = Cliente.objects.filter(creado_por=self.request.user).count()
        context["total_materiales"] = Material.objects.all().count()
        context["ultima_actualizacion_materiales"] = ActualizacionDePreciosDeMateriales.objects.all().order_by(
            'fecha').last()
        context["total_servicios"] = Servicio.objects.all().count()
        context["ultima_actualizacion_servicios"] = ActualizacionDePreciosDeServicios.objects.all().order_by(
            'fecha').last()
        context["total_items"] = Item.objects.all().count()
        context["usuario_id"] = self.request.user.pk
        return context


class PresupuestoDetailView(DetailView):
    model = Presupuesto
    template_name = "admin/presupuestos/presupuesto/presupuesto_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PresupuestoDetailView, self).get_context_data(**kwargs)
        context["detalles"] = DetalleDePresupuesto.objects.filter(presupuesto=self.object)
        context["adicionales"] = AdicionalDePresupuesto.objects.filter(presupuesto=self.object)
        return context


def get_presupuestos_queryset(request, form):
    qs = Presupuesto.objects.filter(cliente__creado_por=request.user)
    if form.cleaned_data.get('numero', ''):
        qs = qs.filter(numero_de_presupuesto__icontains=form.cleaned_data['numero'])
    if form.cleaned_data.get('obra', ''):
        qs = qs.filter(obra__icontains=form.cleaned_data.get('obra', ''))
    if form.cleaned_data.get('cliente', ''):
        qs = qs.filter(cliente__nombre__icontains=form.cleaned_data.get('cliente', ''))
    if form.cleaned_data.get('desde', ''):
        qs = qs.filter(fecha__gte=form.cleaned_data.get('desde', ''))
    if form.cleaned_data.get('hasta', ''):
        qs = qs.filter(fecha__lte=form.cleaned_data.get('hasta', ''))
    if form.cleaned_data.get('ciudad', ''):
        qs = qs.filter(ciudad=form.cleaned_data.get('ciudad', ''))
    if form.cleaned_data.get('estado', ''):
        qs = qs.filter(estado=form.cleaned_data.get('estado', ''))
    return qs


def cambiar_estado_presupuesto(request, pk):
    presupuesto = Presupuesto.objects.get(pk=pk)

    if request.method == "POST":
        if presupuesto.estado == EstadoPresupuestos.PENDIENTE:
            presupuesto.estado = EstadoPresupuestos.ENVIADO
        elif presupuesto.estado == EstadoPresupuestos.ENVIADO:
            nuevo_estado = ""

            try:
                nuevo_estado = request.POST.__getitem__("nuevo_estado")
            except:
                pass

            if "APROBADO" == nuevo_estado:
                presupuesto.estado = EstadoPresupuestos.APROBADO
            elif "RECHAZADO" == nuevo_estado:
                presupuesto.estado = EstadoPresupuestos.RECHAZADO

        presupuesto.save()
        return redirect("/admin/presupuestos/presupuesto")

    numero = presupuesto.numero_de_presupuesto
    mensaje = '¿Desea confirmar la acción?'
    advertencia = 'ADVERTENCIA: esta acción no se puede revertir.'
    ya_enviado = presupuesto.estado == EstadoPresupuestos.ENVIADO
    datos = {"numero": numero, "mensaje": mensaje, "advertencia": advertencia, "ya_enviado": ya_enviado}
    return render(request, "admin/presupuestos/presupuesto/presupuesto_confirm.html", datos)