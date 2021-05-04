from django.conf.urls import url

from cotizaciones.views import SolicitudDetailView, CotizacionesDashboardView, \
    CotizacionDetailView, cancelar_solicitud, concretar_solicitud

urlpatterns = [
    url(r'^solicitud_detail/(?P<pk>\d+)/$',
        SolicitudDetailView.as_view(),
        name='solicitud_detail'
        ),
    url(r'^cancelar_solicitud/(?P<pk>\d+)/$', cancelar_solicitud, name='cancelar_solicitud'),
    url(r'^concretar_solicitud/(?P<pk>\d+)/$', concretar_solicitud, name='concretar_solicitud'),
    url(r'^cotizacion_detail/(?P<pk>\d+)/$',
        CotizacionDetailView.as_view(),
        name='cotizacion_detail'
        ),
    url(r'^cotizaciones_dashboard/$', CotizacionesDashboardView.as_view(), name='cotizaciones_dashboard'),
]

