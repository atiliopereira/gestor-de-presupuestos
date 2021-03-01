from django.contrib import admin

from presupuestos.models import DetalleDePresupuesto, Presupuesto


class DetalleDePresupuestoInlineAdmin(admin.TabularInline):
    model = DetalleDePresupuesto
    autocomplete_fields = ('item', )

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'numero_de_presupuesto', 'obra', 'cliente', 'estado')
    ordering = ('fecha', )
    search_fields = ('numero_de_presupuesto', )
    inlines = (DetalleDePresupuestoInlineAdmin, )
    autocomplete_fields = ('cliente', )
    actions = None


admin.site.register(Presupuesto, PresupuestoAdmin)
