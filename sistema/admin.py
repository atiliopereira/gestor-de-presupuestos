from django.contrib import admin

from sistema.models import Departamento, Ciudad


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', )
    ordering = ('nombre', )
    search_fields = ('nombre', )
    actions = None


admin.site.register(Departamento, DepartamentoAdmin)


class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento',)
    ordering = ('nombre', )
    search_fields = ('nombre', )
    list_filter = ('departamento', )
    actions = None


admin.site.register(Ciudad, CiudadAdmin)
