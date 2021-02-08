from django.contrib import admin

from items.models import Rubro, Item, DetalleDeItem

class RubroAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    ordering = ("nombre",)
    search_fields = ("nombre",)

admin.site.register(Rubro, RubroAdmin)

class ItemAdmin(admin.ModelAdmin):
    ordering = ("descripcion",)
    list_display = ("descripcion", "unidad_de_medida", "rubro")
    search_fields = ("descripcion", "rubro")

admin.site.register(Item, ItemAdmin)

class DetalleDeItemAdmin(admin.ModelAdmin):
    list_display = ("material", "coeficiente")
    ordering = ("material",)
    search_fields = ("material",)

admin.site.register(DetalleDeItem, DetalleDeItemAdmin)
