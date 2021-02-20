from django.contrib import admin
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


admin.site.register(CategoriaDeMaterial, CategoriaDeMaterialAdmin)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'unidad_de_medida', 'categoria', 'ver', 'editar')
    search_fields = ('descripcion', )
    list_filter = ('categoria', )

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
