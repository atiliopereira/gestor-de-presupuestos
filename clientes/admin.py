from django.contrib import admin

from clientes.models import Cliente


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ruc', 'direccion', 'telefono', 'email')
    ordering = ('nombre', )
    search_fields = ('nombre', 'ruc')
    actions = None

    def get_queryset(self, request):
        qs = super(ClienteAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(creado_por=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        obj.save()


admin.site.register(Cliente, ClienteAdmin)
