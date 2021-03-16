from django.contrib import admin
from django.utils.safestring import mark_safe

from cotizaciones.constants import TiposDeCotizacion
from cotizaciones.models import Solicitud
from presupuestos.forms import DetalleDePresupuestoForm, PresupuestoForm, PresupuestoSearchForm
from presupuestos.models import DetalleDePresupuesto, Presupuesto
from presupuestos.models import get_siguiente_numero_de_presupuesto, get_siguiente_numero_de_revision
from presupuestos.constants import EstadoPresupuestos
from presupuestos.views import get_presupuestos_queryset


class DetalleDePresupuestoInlineAdmin(admin.TabularInline):
    model = DetalleDePresupuesto
    form = DetalleDePresupuestoForm

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


class DetalleDePresupuestoAdmin(admin.ModelAdmin):
    list_display = ('presupuesto', 'item', 'cantidad', 'subtotal')
    search_fields = ('presupuesto', 'item')
    autocomplete_fields = ('presupuesto', 'item')
    actions = None


admin.site.register(DetalleDePresupuesto, DetalleDePresupuestoAdmin)


class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('editar', 'ver', 'fecha', 'numero_de_presupuesto', 'obra', 'cliente', 'estado', 'cambiar_estado',
                    'imprimir', 'cotizar_materiales', 'cotizar_servicios')
    ordering = ('-fecha', )
    search_fields = ('numero_de_presupuesto', )
    inlines = (DetalleDePresupuestoInlineAdmin, )
    autocomplete_fields = ('cliente', )
    form = PresupuestoForm
    actions = None

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js', 'js/admin/presupuesto/presupuesto.js',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.numero_de_presupuesto = get_siguiente_numero_de_presupuesto(request.user)
            super().save_model(request, obj, form, change)
        elif obj.estado != EstadoPresupuestos.PENDIENTE:
            detalles = DetalleDePresupuesto.objects.filter(presupuesto=obj)
            obj.pk = None
            obj.numero_de_presupuesto = get_siguiente_numero_de_revision(obj.numero_de_presupuesto)
            super().save_model(request, obj, form, False)

            for detalle in detalles:
                detalle.presupuesto = obj
                detalle.pk = None
                detalle.save()
        else:
            super().save_model(request, obj, form, change)

    def editar(self, obj):
        html = '<a href="/admin/presupuestos/presupuesto/{}" class="icon-block"><i class="fa fa-edit"></i></a>'.format(obj.pk)
        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/presupuestos/presupuesto_detail/{}" class="icon-block"><i class="fa fa-eye"></i></a>'.format(obj.pk)
        return mark_safe(html)

    def cambiar_estado(self, obj):

        if obj.estado == EstadoPresupuestos.PENDIENTE or obj.estado == EstadoPresupuestos.ENVIADO:
            html = f'<a href="/admin/presupuestos/cambiar_estado_presupuesto/{obj.pk}" class="icon-block">CAMBIAR ESTADO</a>'
        else:
            html = ""
        return mark_safe(html)

    def imprimir(self, obj):
        html = '<a href="/admin/presupuestos/presupuesto_report/%s" class="icon-block"> <i class="fa fa-file-excel-o" style="color:green; font-size: 1.73em; padding-left:10px"></i> Presupuesto</a>' % obj.pk
        html += '<a href="/admin/presupuestos/presupuesto_servicios_report/%s" class="icon-block"> <i class="fa fa-file-excel-o" style="color:green; font-size: 1.73em; padding-left:30px"></i> Mano de Obra</a>' % obj.pk
        html += '<a href="/admin/presupuestos/presupuesto_materiales_report/%s" class="icon-block"> <i class="fa fa-file-excel-o" style="color:green; font-size: 1.73em; padding-left:30px"></i> Materiales</a>' % obj.pk

        return mark_safe(html)

    def cotizar_materiales(self, obj):
        tipo = TiposDeCotizacion.MATERIAL
        html = 'Solicitado'
        solicitudes = Solicitud.objects.filter(presupuesto=obj).filter(tipo=TiposDeCotizacion.MATERIAL)
        if not solicitudes:
            html = f'<a href="/admin/cotizaciones/solicitud/add/?next=/admin/cotizaciones/solicitud/&presupuesto={obj.pk}&tipo={tipo}" class="icon-block">SOLICITAR</a>'
        return mark_safe(html)

    def cotizar_servicios(self, obj):
        tipo = TiposDeCotizacion.SERVICIOS
        html = 'Solicitado'
        solicitudes = Solicitud.objects.filter(presupuesto=obj).filter(tipo=TiposDeCotizacion.SERVICIOS)
        if not solicitudes:
            html = f'<a href="/admin/cotizaciones/solicitud/add/?next=/admin/cotizaciones/solicitud/&presupuesto={obj.pk}&tipo={tipo}" class="icon-block">SOLICITAR</a>'
        return mark_safe(html)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct

    def lookup_allowed(self, lookup, *args, **kwargs):
        if lookup in self.advanced_search_form.fields.keys():
            return True
        return super(PresupuestoAdmin, self).lookup_allowed(lookup, *args, **kwargs)

    def get_queryset(self, request):
        form = getattr(self, 'advanced_search_form', None)
        if form:
            qs = get_presupuestos_queryset(request, form)
        else:
            qs = super(PresupuestoAdmin, self).get_queryset(request)
        return qs

    def changelist_view(self, request, extra_context=None, **kwargs):

        self.my_request_get = request.GET.copy()
        self.advanced_search_form = PresupuestoSearchForm(request.GET)
        self.advanced_search_form.is_valid()
        self.other_search_fields = {}
        params = request.get_full_path().split('?')
        extra_context = extra_context or {}
        extra_context.update({'asf': PresupuestoSearchForm,
                              'my_request_get': self.my_request_get,
                              'params': '?%s' % params[1].replace('%2F', '/') if len(params) > 1 else ''
                              })
        request.GET._mutable = True

        for key in self.advanced_search_form.fields.keys():
            try:
                temp = request.GET.pop(key)
            except KeyError:
                pass
            else:
                if temp != ['']:
                    self.other_search_fields[key] = temp
        request.GET_mutable = False

        return super(PresupuestoAdmin, self) \
            .changelist_view(request, extra_context=extra_context, **kwargs)


admin.site.register(Presupuesto, PresupuestoAdmin)
