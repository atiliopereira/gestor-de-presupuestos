from django.contrib import admin
from materiales.models import ActualizacionDePrecios, PrecioDeMaterial
from django.utils.safestring import mark_safe

from materiales.models import UnidadDeMedida, CategoriaDeMaterial, Material


class UnidadDeMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'simbolo')
    ordering = ('nombre',)
    search_fields = ('nombre', 'simbolo')


admin.site.register(UnidadDeMedida, UnidadDeMedidaAdmin)


class CategoriaDeMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'get_categoria_principal')
    search_fields = ('nombre', 'categoria', )
    ordering = ('nombre', )
    autocomplete_fields = ('categoria_padre',)
    actions = None


admin.site.register(CategoriaDeMaterial, CategoriaDeMaterialAdmin)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('editar', 'ver', 'codigo', 'descripcion', 'unidad_de_medida', 'categoria',)
    search_fields = ('descripcion', 'codigo')
    list_filter = ('categoria', )
    actions = None

    def editar(self, obj):
        html = '<a href="/admin/materiales/material/%s" '
        html += 'class="icon-block"> <i class="fa fa-edit"></i></a>'
        html %= obj.pk

        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/materiales/material_detail/%s" '
        html += 'class="icon-block"> <i class="fa fa-eye"></i></a>'
        html %= obj.pk

        return mark_safe(html)


admin.site.register(Material, MaterialAdmin)


class PrecioDeMaterialAdmin(admin.ModelAdmin):
    list_display = ('material', 'precio', 'ciudad', 'inicio_de_vigencia', 'fin_de_vigencia')
    search_fields = ('material__descripcion', )
    list_filter = ('ciudad', )
    autocomplete_fields = ('material', )

    actions = None


admin.site.register(PrecioDeMaterial, PrecioDeMaterialAdmin)


class ActualizacionDePreciosAdmin(admin.ModelAdmin):
    list_display = ('fecha', )
    actions = None


admin.site.register(ActualizacionDePrecios, ActualizacionDePreciosAdmin)