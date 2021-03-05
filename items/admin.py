from django.contrib import admin
from django.utils.safestring import mark_safe
from items.models import Rubro, Item, DetalleDeItem


class DetalleDeItemInlineAdmin(admin.TabularInline):
    model = DetalleDeItem
    autocomplete_fields = ("material",)
    extra = 0


class RubroAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    ordering = ("nombre",)
    search_fields = ("nombre",)
    actions = None


admin.site.register(Rubro, RubroAdmin)


class ItemAdmin(admin.ModelAdmin):
    ordering = ("descripcion",)
    list_display = ('editar', 'ver', "descripcion", "unidad_de_medida", "rubro")
    search_fields = ("descripcion", "rubro")
    autocomplete_fields = ("rubro",)
    inlines = (DetalleDeItemInlineAdmin,)
    actions = None

    def editar(self, obj):
        html = '<a href="/admin/items/item/{}" class="icon-block"><i class="fa fa-edit"></i></a>'.format(obj.pk)
        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/items/item_detail/{}" class="icon-block"><i class="fa fa-eye"></i></a>'.format(obj.pk)
        return mark_safe(html)


admin.site.register(Item, ItemAdmin)


