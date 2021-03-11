from django.conf.urls import url

from clientes.views import ClienteDetailView

urlpatterns = [
    url(r'^cliente_detail/(?P<pk>\d+)/$', ClienteDetailView.as_view(), name='cliente_detail')
]