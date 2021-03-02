from django.http.response import JsonResponse

from items.models import Item


def get_item(request):
    item_id = (request.GET['item_id']).replace(" ", "")
    datos = {}

    if item_id == "":
        return JsonResponse(datos)

    item = Item.objects.get(id=item_id)
    precio = item.get_precio_unitario()
    datos.update({'precio': int(precio)})

    return JsonResponse(datos)
