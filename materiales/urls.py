from django.conf.urls import url

from materiales.views import MaterialDetailView

urlpatterns = [
    url(r'^material_detail/(?P<pk>\d+)/$', MaterialDetailView.as_view(), name='material_detail')
]