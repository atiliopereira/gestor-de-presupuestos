from django.conf.urls import url

from items.ajax import get_item
from items.autocomplete import ItemAutocomplete

urlpatterns = [
    url(
        r'^item-autocomplete/$',
        ItemAutocomplete.as_view(),
        name='item-autocomplete',
    ),
    url('getitem/$', get_item),
]

