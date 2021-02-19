import datetime
from django.shortcuts import render
from django.views.generic import DetailView
from materiales.models import Material, PrecioDeMaterial, get_precio_de_material

class MaterialDetailView(DetailView):
    model = Material
    template_name = "admin/materiales/material/material_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MaterialDetailView, self).get_context_data(**kwargs)
        lista = PrecioDeMaterial.objects.filter(material=self.object).order_by("-inicio_de_vigencia")
        context["precios"] = lista
        precio_mat_hoy = get_precio_de_material(material=self.object)
        
        if precio_mat_hoy:
            context["precio_actual"] = precio_mat_hoy.precio
            for index in range(0, len(lista)):
                if precio_mat_hoy == lista[index]:
                    lista[index].es_actual = True
                    break
        
        return context

