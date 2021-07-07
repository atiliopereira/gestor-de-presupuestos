from django.shortcuts import render
from django.views.generic import DetailView

from items.models import Item, MaterialDeItem, ServicioDeItem, get_precio_unitario_de_item
from sistema.models import Ciudad


class ItemDetailView(DetailView):
    model = Item
    template_name = "admin/items/item/item_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context["materiales"] = MaterialDeItem.objects.filter(item=self.object)
        context["servicios"] = ServicioDeItem.objects.filter(item=self.object)
        context["precios"] = [[ciudad, get_precio_unitario_de_item(self.object, ciudad)] for ciudad in Ciudad.objects.all()]
        return context
