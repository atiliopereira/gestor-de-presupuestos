from django.contrib import admin
from django.utils.safestring import mark_safe
from items.models import Rubro, Item, MaterialDeItem, ServicioDeItem


class MaterialDeItemInlineAdmin(admin.TabularInline):
    model = MaterialDeItem
    autocomplete_fields = ("material",)
    extra = 0


class ServicioDeItemInlineAdmin(admin.TabularInline):
    model = ServicioDeItem
    autocomplete_fields = ("servicio",)
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
    search_fields = ("descripcion", )
    autocomplete_fields = ("rubro",)
    inlines = (MaterialDeItemInlineAdmin, ServicioDeItemInlineAdmin)
    actions = None

    def editar(self, obj):
        html = '<a href="/admin/items/item/{}" class="icon-block"><i class="fa fa-edit"></i></a>'.format(obj.pk)
        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/items/item_detail/{}" class="icon-block"><i class="fa fa-eye"></i></a>'.format(obj.pk)
        return mark_safe(html)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


admin.site.register(Item, ItemAdmin)
