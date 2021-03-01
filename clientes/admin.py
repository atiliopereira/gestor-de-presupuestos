from django.contrib import admin

from clientes.models import Cliente


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ruc', 'direccion', 'telefono', 'email', 'creado_por')
    ordering = ('nombre', )
    search_fields = ('nombre', 'ruc')
    actions = None

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        obj.save()


admin.site.register(Cliente, ClienteAdmin)
