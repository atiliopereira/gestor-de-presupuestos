from django.contrib import admin
from django.utils.safestring import mark_safe

from clientes.models import Cliente


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('editar', 'ver', 'nombre', 'ruc', 'direccion', 'telefono', 'email')
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

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def editar(self, obj):
        html = '<a href="/admin/clientes/cliente/{}" class="icon-block"><i class="fa fa-edit"></i></a>'.format(obj.pk)
        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/clientes/cliente_detail/{}" class="icon-block"><i class="fa fa-eye"></i></a>'.format(obj.pk)
        return mark_safe(html)


admin.site.register(Cliente, ClienteAdmin)
