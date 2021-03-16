from django.conf.urls import url

from cotizaciones.views import crear_solicitud, SolicitudDetailView

urlpatterns = [
    url(r'^solicitud_detail/(?P<pk>\d+)/$',
        SolicitudDetailView.as_view(),
        name='solicitud_detail'
        ),
    url(r'^solicitar_cotizacion/(?P<pk>(\d+))/(?P<tipo>(\d+))/$',
        crear_solicitud,
        name='solicitad_cotizacion'
        ),
]
