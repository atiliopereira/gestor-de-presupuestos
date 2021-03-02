from django.contrib import admin

from presupuestos.forms import DetalleDePresupuestoForm, PresupuestoForm
from presupuestos.models import DetalleDePresupuesto, Presupuesto


class DetalleDePresupuestoInlineAdmin(admin.TabularInline):
    model = DetalleDePresupuesto
    form = DetalleDePresupuestoForm

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
    form = PresupuestoForm
    actions = None

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js', 'js/admin/presupuesto/presupuesto.js',)


admin.site.register(Presupuesto, PresupuestoAdmin)
