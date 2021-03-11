from django.contrib import admin
from django.utils.safestring import mark_safe

from servicios.models import CategoriaDeServicio, Servicio, PrecioDeServicio, ActualizacionDePreciosDeServicios


class CategoriaDeServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'get_categoria_principal')
    search_fields = ('nombre', 'categoria', )
    ordering = ('nombre', )
    autocomplete_fields = ('categoria_padre',)
    actions = None


admin.site.register(CategoriaDeServicio, CategoriaDeServicioAdmin)


class ServicioAdmin(admin.ModelAdmin):
    list_display = ('editar', 'ver', 'codigo', 'descripcion', 'unidad_de_medida', 'categoria',)
    search_fields = ('descripcion', 'codigo')
    list_filter = ('categoria', )
    actions = None

    def editar(self, obj):
        html = '<a href="/admin/servicios/servicio/%s" '
        html += 'class="icon-block"> <i class="fa fa-edit"></i></a>'
        html %= obj.pk

        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/mservicios/servicio_detail/%s" '
        html += 'class="icon-block"> <i class="fa fa-eye"></i></a>'
        html %= obj.pk

        return mark_safe(html)


admin.site.register(Servicio, ServicioAdmin)


class PrecioDeServicioAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'precio', 'ciudad', 'inicio_de_vigencia', 'fin_de_vigencia')
    search_fields = ('servicio__descripcion', )
    list_filter = ('ciudad', )
    autocomplete_fields = ('servicio', )

    actions = None


admin.site.register(PrecioDeServicio, PrecioDeServicioAdmin)


class ActualizacionDePreciosDeServiciosAdmin(admin.ModelAdmin):
    list_display = ('fecha', )
    actions = None


admin.site.register(ActualizacionDePreciosDeServicios, ActualizacionDePreciosDeServiciosAdmin)