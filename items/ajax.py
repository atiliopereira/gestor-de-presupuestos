from django.http.response import JsonResponse

from items.models import Item, get_precio_unitario_de_item
from sistema.models import Ciudad


def get_item(request):
    item_id = (request.GET['item_id']).replace(" ", "")
    ciudad_id = (request.GET['ciudad_id']).replace(" ", "")
    datos = {}

    if item_id == "":
        return JsonResponse(datos)

    item = Item.objects.get(pk=item_id)
    ciudad = Ciudad.objects.get(pk=ciudad_id)
    precio = get_precio_unitario_de_item(item, ciudad)
    datos.update({'precio': int(precio)})

    return JsonResponse(datos)
