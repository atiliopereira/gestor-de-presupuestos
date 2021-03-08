from dal import autocomplete

from items.models import Item


class ItemAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Item.objects.all()
        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)
        return qs
