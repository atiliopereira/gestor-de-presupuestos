from django.conf.urls import url

from presupuestos.reports import presupuesto_report, presupuesto_materiales_report, presupuesto_servicios_report
from presupuestos.views import PresupuestoDetailView, PresupuestoDashboardView

urlpatterns = [
    url(r'^presupuesto_detail/(?P<pk>\d+)/$', PresupuestoDetailView.as_view(), name='presupuesto_detail'),
    url(r'^presupuesto_dashboard/$', PresupuestoDashboardView.as_view(), name='presupuesto_dashboard'),
    url(
            r'^presupuesto_report/(?P<id>\w+)/$',
            presupuesto_report,
            name='presupuesto',
        ),
    url(
            r'^presupuesto_materiales_report/(?P<id>\w+)/$',
            presupuesto_materiales_report,
            name='presupuesto_materiales',
        ),
    url(
            r'^presupuesto_servicios_report/(?P<id>\w+)/$',
            presupuesto_servicios_report,
            name='presupuesto_servicios',
        ),
]
