import datetime

from django.views.generic import DetailView

from servicios.models import Servicio, PrecioDeServicio, ActualizacionDePreciosDeServicios
from sistema.models import Ciudad


class ServicioDetailView(DetailView):
    model = Servicio
    template_name = "admin/servicios/servicio/detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(ServicioDetailView, self).get_context_data(**kwargs)
        context["precios"] = PrecioDeServicio.objects.filter(servicio=self.object).order_by("-inicio_de_vigencia")
        context["ciudades"] = [ciudad for ciudad in Ciudad.objects.all() if PrecioDeServicio.objects.filter(servicio=self.object).filter(ciudad=ciudad).exists()]
        context["hoy"] = datetime.date.today()
        return context


class ActualizacionDePreciosDeServiciosDetailView(DetailView):
    model = ActualizacionDePreciosDeServicios
    template_name = "admin/servicios/actualizaciondepreciosdeservicios/detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(ActualizacionDePreciosDeServiciosDetailView, self).get_context_data(**kwargs)
        return context
