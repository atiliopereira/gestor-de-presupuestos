from django.conf.urls import url

from servicios.views import ServicioDetailView, ActualizacionDePreciosDeServiciosDetailView

urlpatterns = [
    url(r'^servicio_detail/(?P<pk>\d+)/$', ServicioDetailView.as_view(), name='servicio_detail'),
    url(
        r'^actualizacionservicio_detail/(?P<pk>\d+)/$',
        ActualizacionDePreciosDeServiciosDetailView.as_view(),
        name='actualizacionservicio_detail'
    )
]
