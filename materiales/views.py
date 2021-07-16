import datetime

from django.views.generic import DetailView

from materiales.models import Material, PrecioDeMaterial, ActualizacionDePreciosDeMateriales
from sistema.models import Ciudad


class MaterialDetailView(DetailView):
    model = Material
    template_name = "admin/materiales/material/material_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MaterialDetailView, self).get_context_data(**kwargs)
        context["precios"] = PrecioDeMaterial.objects.filter(material=self.object).order_by("-inicio_de_vigencia")
        context["ciudades"] = [ciudad for ciudad in Ciudad.objects.all() if PrecioDeMaterial.objects.filter(material=self.object).filter(ciudad=ciudad).exists()]
        context["hoy"] = datetime.date.today()
        return context


class ActualizacionDePreciosDeMaterialesDetailView(DetailView):
    model = ActualizacionDePreciosDeMateriales
    template_name = "admin/materiales/actualizaciondepreciosdemateriales/detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(ActualizacionDePreciosDeMaterialesDetailView, self).get_context_data(**kwargs)
        return context
