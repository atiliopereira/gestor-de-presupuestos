from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from sistema.models import Departamento, Ciudad, Usuario


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', )
    ordering = ('nombre', )
    search_fields = ('nombre', )
    actions = None


admin.site.register(Departamento, DepartamentoAdmin)


class CiudadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'departamento',)
    ordering = ('nombre', )
    search_fields = ('nombre', )
    list_filter = ('departamento', )
    actions = None


admin.site.register(Ciudad, CiudadAdmin)


class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
