from django.contrib import admin
from django.utils.safestring import mark_safe

from cotizaciones.forms import SolicitudSearchForm, SolicitudForm
from cotizaciones.models import DetalleDeSolicitud, Solicitud, Cotizacion
from cotizaciones.views import get_solicitudes_queryset


class DetalleDeSolicitudInlineAdmin(admin.TabularInline):
    model = DetalleDeSolicitud
    autocomplete_fields = ('detalle_de_presupuesto', )

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


class SolicitudAdmin(admin.ModelAdmin):
    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js', 'solicitud.js',)
    list_display = ('ver', 'id', 'fecha', 'vencimiento', 'tipo', 'get_ciudad')
    search_fields = ('presupuesto', )
    autocomplete_fields = ('presupuesto', )
    form = SolicitudForm
    filter_horizontal = ('proveedores', 'profesionales')
    actions = None
    def ver(self, obj):
        html = '<a href="/admin/cotizaciones/solicitud_detail/{}" class="icon-block"><i class="fa fa-eye"></i></a>'.format(obj.pk)
        return mark_safe(html)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct

    def lookup_allowed(self, lookup, *args, **kwargs):
        if lookup in self.advanced_search_form.fields.keys():
            return True
        return super(SolicitudAdmin, self).lookup_allowed(lookup, *args, **kwargs)

    def get_queryset(self, request):
        form = getattr(self, 'advanced_search_form', None)
        qs = super(SolicitudAdmin, self).get_queryset(request)
        if form:
            qs = get_solicitudes_queryset(request, form)
        return qs

    def changelist_view(self, request, extra_context=None, **kwargs):

        self.my_request_get = request.GET.copy()
        self.advanced_search_form = SolicitudSearchForm(request.GET)
        self.advanced_search_form.is_valid()
        self.other_search_fields = {}
        params = request.get_full_path().split('?')

        extra_context = extra_context or {}
        extra_context.update({'asf': SolicitudSearchForm,
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

        return super(SolicitudAdmin, self) \
            .changelist_view(request, extra_context=extra_context, **kwargs)


admin.site.register(Solicitud, SolicitudAdmin)


class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'solicitud')
    search_fields = ('solicitud',)
    autocomplete_fields = ('solicitud',)
    actions = None


admin.site.register(Cotizacion, CotizacionAdmin)

