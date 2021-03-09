from django.contrib import admin
from django.utils.safestring import mark_safe

from profesionales.models import Servicio, ServicioProfesional, Profesional, MaterialProveedor, Proveedor


class ServicioAdmin(admin.ModelAdmin):
    search_fields = ('descripcion', )
    list_display = ('descripcion', )
    actions = None


admin.site.register(Servicio, ServicioAdmin)


class ServicioProfesionalInlineAdmin(admin.TabularInline):
    model = ServicioProfesional
    autocomplete_fields = ('servicio', )
    extra = 1


class ProfesionalAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'ruc', 'direccion', 'telefono', 'email')
    list_display = ('editar', 'nombre', 'ruc', 'direccion', 'ciudad', 'telefono', 'email', 'get_servicios')
    inlines = (ServicioProfesionalInlineAdmin, )
    actions = None

    def editar(self, obj):
        html = '<a href="/admin/profesionales/profesional/{}" class="icon-block"><i class="fa fa-edit"></i></a>'.format(obj.pk)
        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/profesionales/profesional_detail/{}" class="icon-block"><i class="fa fa-eye"></i></a>'.format(obj.pk)
        return mark_safe(html)


admin.site.register(Profesional, ProfesionalAdmin)


class MaterialProveedorInlineAdmin(admin.TabularInline):
    model = MaterialProveedor
    autocomplete_fields = ('material', )
    extra = 1


class ProveedorAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'ruc', 'direccion', 'telefono', 'email')
    list_display = ('editar', 'nombre', 'ruc', 'direccion', 'ciudad', 'telefono', 'email', 'get_materiales')
    inlines = (MaterialProveedorInlineAdmin, )
    actions = None

    def editar(self, obj):
        html = '<a href="/admin/profesionales/proveedor/{}" class="icon-block"><i class="fa fa-edit"></i></a>'.format(obj.pk)
        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/profesionales/proveedor_detail/{}" class="icon-block"><i class="fa fa-eye"></i></a>'.format(obj.pk)
        return mark_safe(html)


admin.site.register(Proveedor, ProveedorAdmin)