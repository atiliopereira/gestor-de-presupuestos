from django.conf.urls import url

from presupuestos.views import PresupuestoDetailView, PresupuestoDashboardView

urlpatterns = [
    url(r'^presupuesto_detail/(?P<pk>\d+)/$', PresupuestoDetailView.as_view(), name='presupuesto_detail'),
    url(r'^presupuesto_dashboard/$', PresupuestoDashboardView.as_view(), name='presupuesto_dashboard'),
]