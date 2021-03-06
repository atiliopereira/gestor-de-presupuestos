from django.conf.urls import url

from items.ajax import get_item
from items.autocomplete import ItemCiudadAutocomplete
from items.views import ItemDetailView


urlpatterns = [
    url(
        r'^item-autocomplete/$',
        ItemCiudadAutocomplete.as_view(),
        name='item-autocomplete',
    ),
    url('getitem/$', get_item),
    url(r'^item_detail/(?P<pk>\d+)/$', ItemDetailView.as_view(), name='item_detail')
]
