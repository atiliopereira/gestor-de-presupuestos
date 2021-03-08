from django.contrib import admin
from django.utils.safestring import mark_safe

from profesionales.models import Servicio, ServicioProfesional, Profesional


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
    list_display = ('editar', 'nombre', 'ruc', 'direccion', 'telefono', 'email')
    inlines = (ServicioProfesionalInlineAdmin, )
    actions = None

    def editar(self, obj):
        html = '<a href="/admin/profesionales/profesional/{}" class="icon-block"><i class="fa fa-edit"></i></a>'.format(obj.pk)
        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/profesionales/profesional_detail/{}" class="icon-block"><i class="fa fa-eye"></i></a>'.format(obj.pk)
        return mark_safe(html)


admin.site.register(Profesional, ProfesionalAdmin)