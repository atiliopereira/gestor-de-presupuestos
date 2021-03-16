from django.conf.urls import url

from presupuestos.reports import presupuesto_excel, presupuesto_materiales_report, presupuesto_servicios_report, \
    presupuesto_pdf
from presupuestos.views import PresupuestoDetailView, PresupuestoDashboardView, cambiar_estado_presupuesto

urlpatterns = [
    url(r'^presupuesto_detail/(?P<pk>\d+)/$', PresupuestoDetailView.as_view(), name='presupuesto_detail'),
    url(r'^presupuesto_dashboard/$', PresupuestoDashboardView.as_view(), name='presupuesto_dashboard'),
    url(
            r'^presupuesto_excel/(?P<id>\w+)/$',
            presupuesto_excel,
            name='presupuesto_excel',
        ),
    url(
            r'^presupuesto_pdf/(?P<id>\w+)/$',
            presupuesto_pdf,
            name='presupuesto_pdf',
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
    url(r'^cambiar_estado_presupuesto/(?P<pk>\d+)/$',
            cambiar_estado_presupuesto,
            name='cambiar_estado_presupuesto'),
]