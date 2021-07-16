from django.conf.urls import url

from materiales.views import MaterialDetailView, ActualizacionDePreciosDeMaterialesDetailView

urlpatterns = [
    url(r'^material_detail/(?P<pk>\d+)/$', MaterialDetailView.as_view(), name='material_detail'),
    url(
        r'^actualizacionmaterial_detail/(?P<pk>\d+)/$',
        ActualizacionDePreciosDeMaterialesDetailView.as_view(),
        name='actualizacionmaterial_detail'
    )
]
