from django.views.generic import DetailView, TemplateView

from clientes.models import Cliente
from items.models import Item
from materiales.models import Material, ActualizacionDePrecios
from presupuestos.models import Presupuesto, DetalleDePresupuesto


class PresupuestoDashboardView(TemplateView):
    template_name = 'presupuesto_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(PresupuestoDashboardView, self).get_context_data(**kwargs)
        context["total_presupuestos"] = Presupuesto.objects.filter(cliente__creado_por=self.request.user).count()
        context["total_clientes"] = Cliente.objects.filter(creado_por=self.request.user).count()
        context["total_materiales"] = Material.objects.all().count()
        context["ultima_actualizacion"] = ActualizacionDePrecios.objects.all().order_by('fecha').last()
        context["total_items"] = Item.objects.all().count()
        context["usuario_id"] = self.request.user.pk
        return context


class PresupuestoDetailView(DetailView):
    model = Presupuesto
    template_name = "admin/presupuestos/presupuesto/presupuesto_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PresupuestoDetailView, self).get_context_data(**kwargs)
        context["detalles"] = DetalleDePresupuesto.objects.filter(presupuesto=self.object)
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