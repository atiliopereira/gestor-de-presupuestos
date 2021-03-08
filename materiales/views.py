import datetime

from django.shortcuts import render
from django.views.generic import DetailView

from materiales.models import Material, PrecioDeMaterial, get_precio_de_material

class MaterialDetailView(DetailView):
    model = Material
    template_name = "admin/materiales/material/material_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MaterialDetailView, self).get_context_data(**kwargs)
        context["precios"] = PrecioDeMaterial.objects.filter(material=self.object).order_by("-inicio_de_vigencia")
        context["precio_material_hoy"] = self.object.precio_actual()
        context["hoy"] = datetime.date.today()
        return context
