from django.shortcuts import render
from django.views.generic import DetailView

from clientes.models import Cliente
from presupuestos.models import Presupuesto


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "admin/clientes/cliente/cliente_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        context["presupuestos"] = Presupuesto.objects.filter(cliente=self.object)
        return context

