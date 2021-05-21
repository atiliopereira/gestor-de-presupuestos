from django.contrib import admin
from django.utils.safestring import mark_safe

from servicios.models import CategoriaDeServicio, Servicio, PrecioDeServicio, ActualizacionDePreciosDeServicios, \
    actualizar_precios_de_servicios


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
    list_display = ('editar', 'ver', 'id', 'fecha', 'lineas', 'creados', 'actualizados', 'estado')
    actions = None

    def editar(self, obj):
        # Se mantiene solamente por coherencia de interfaz entre listas
        return ''

    def ver(self, obj):
        html = '<a href="/admin/servicios/actualizacionservicio_detail/%s" '
        html += 'class="icon-block"> <i class="fa fa-eye"></i></a>'
        html %= obj.pk

        return mark_safe(html)

    def estado(self, obj):
        if obj.error:
            html = '<span class="label" style="background-color: #f44336; font-weight: bold; color: white; padding: 4px; border-radius: 3px;">ERROR</span>'
        else:
            html = '<span class="label" style="background-color: #28a745; font-weight: bold; color: white; padding: 4px; border-radius: 3px;">PROCESADO</span>'
        return mark_safe(html)

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            actualizar_precios_de_servicios(obj)


admin.site.register(ActualizacionDePreciosDeServicios, ActualizacionDePreciosDeServiciosAdmin)