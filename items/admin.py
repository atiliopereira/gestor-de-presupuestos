from django.contrib import admin

from items import Rubro, Item, DetalleDeItem

class RubroAdmin
    list_display = ("nombre",)
    ordering = ("nombre",)
    search_fields = ("nombre",)

admin.site.register(Rubro, RubroAdmin)
