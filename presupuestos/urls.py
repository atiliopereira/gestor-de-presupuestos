from django.conf.urls import url

from presupuestos.views import PresupuestoDetailView


urlpatterns = [
    url(r'^presupuesto_detail/(?P<pk>\d+)/$', PresupuestoDetailView.as_view(), name='presupuesto_detail')
]