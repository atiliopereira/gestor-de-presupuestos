from django.contrib import admin

from materiales.models import UnidadDeMedida, CategoriaDeMaterial, Material


class UnidadDeMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'simbolo')
    ordering = ('nombre',)
    search_fields = ('nombre', 'simbolo')


admin.site.register(UnidadDeMedida, UnidadDeMedidaAdmin)


class CategoriaDeMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria_principal')
    search_fields = ('nombre', 'categoria', )
    ordering = ('nombre', )


admin.site.register(CategoriaDeMaterial, CategoriaDeMaterialAdmin)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'unidad_de_medida', 'categoria')
    search_fields = ('descripcion', )
    list_filter = ('categoria', )


admin.site.register(Material, MaterialAdmin)