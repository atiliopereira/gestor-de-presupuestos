from dal import autocomplete

from items.models import Item, get_precio_unitario_de_item


class ItemAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Item.objects.none()
        qs = Item.objects.all()
        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)
        return qs


class ItemCiudadAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ItemAutocomplete.get_queryset(self)
        try:
            # filtrar items que tengan costo mayor que creo en la ciudad específica.
            ciudad_pk = int(self.forwarded['ciudad'])
            qs = qs.filter(pk__in=[i.pk for i in Item.objects.all() if get_precio_unitario_de_item(i.pk, ciudad_pk)])
        except Exception as e:
            qs = qs.none()
        return qs
