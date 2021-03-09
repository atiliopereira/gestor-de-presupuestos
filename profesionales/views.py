from django.views.generic import TemplateView

from profesionales.models import Profesional, Proveedor


class ProfesionalesDashboardView(TemplateView):
    template_name = 'profesionales_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(ProfesionalesDashboardView, self).get_context_data(**kwargs)
        context["total_profesionales"] = Profesional.objects.all().count()
        context["total_proveedores"] = Proveedor.objects.all().count()
        return context
