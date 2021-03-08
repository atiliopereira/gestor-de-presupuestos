from django.shortcuts import render
from django.views.generic import DetailView

from items.models import Item, DetalleDeItem

class ItemDetailView(DetailView):
    model = Item
    template_name = "admin/items/item/item_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context["detalles"] = DetalleDeItem.objects.filter(item=self.object)
        return context
