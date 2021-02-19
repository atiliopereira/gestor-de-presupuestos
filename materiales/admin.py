from django.contrib import admin
from materiales.models import UnidadDeMedida, CategoriaDeMaterial, Material, ActualizacionDePrecios


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
    list_display = ('codigo', 'descripcion', 'unidad_de_medida', 'categoria', 'precio_actual',)
    search_fields = ('descripcion', )
    list_filter = ('categoria', )
    actions = None


admin.site.register(Material, MaterialAdmin)


class ActualizacionDePreciosAdmin(admin.ModelAdmin):
    list_display = ('fecha', )
    actions = None


admin.site.register(ActualizacionDePrecios, ActualizacionDePreciosAdmin)