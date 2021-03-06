from django.shortcuts import render
from django.views.generic import DetailView

from presupuestos.models import Presupuesto, DetalleDePresupuesto

class PresupuestoDetailView(DetailView):
    model = Presupuesto
    template_name = "admin/presupuestos/presupuesto/presupuesto_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PresupuestoDetailView, self).get_context_data(**kwargs)
        context["detalles"] = DetalleDePresupuesto.objects.filter(presupuesto=self.object)
        return context
