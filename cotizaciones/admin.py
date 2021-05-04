from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe

from cotizaciones.constants import TiposDeCotizacion, EstadoDeSolicitud
from cotizaciones.forms import SolicitudSearchForm, SolicitudForm, CotizacionForm, MaterialDeCotizacionForm, \
    ServicioDeCotizacionForm
from cotizaciones.models import DetalleDeSolicitud, Solicitud, Cotizacion, MaterialDeCotizacion, ServicioDeCotizacion
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
    list_display = ('ver', 'id', 'fecha', 'vencimiento', 'tipo', 'get_ciudad', 'get_cotizaciones', 'estado',
                    'concretar', 'cancelar')
    search_fields = ('presupuesto', )
    autocomplete_fields = ('presupuesto', )
    form = SolicitudForm
    filter_horizontal = ('proveedores', 'profesionales')
    inlines = (DetalleDeSolicitudInlineAdmin, )
    actions = None

    def ver(self, obj):
        html = '<a href="/admin/cotizaciones/solicitud_detail/{}" class="icon-block"><i class="fa fa-eye"></i></a>'.format(obj.pk)
        return mark_safe(html)

    def concretar(self, obj):
        if obj.estado == EstadoDeSolicitud.VIGENTE:
            html = '<a href="/admin/cotizaciones/concretar_solicitud/%s" class="icon-block"> <i class="fa fa-thumbs-up fa-2x" style="color:green"></i></a>' % obj.pk
        else:
            html = ''
        return mark_safe(html)

    def cancelar(self, obj):
        if obj.estado == EstadoDeSolicitud.VIGENTE:
            html = '<a href="/admin/cotizaciones/cancelar_solicitud/%s" class="icon-block"> <i class="fa fa-thumbs-down fa-2x" style="color:red"></i></a>' % obj.pk
        else:
            html = ''
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


class MaterialDeCotizacionInlineAdmin(admin.TabularInline):
    model = MaterialDeCotizacion
    form = MaterialDeCotizacionForm
    max_num = 0

    def get_extra(self, request, obj=None, **kwargs):
        return 0

    def get_formset(self, request, obj=None, **kwargs):
        """
        Override the formset function in order to remove the add, change and remove buttons beside the foreign
        key pull-down menus in the inline.
        """
        formset = super(MaterialDeCotizacionInlineAdmin, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['material'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_delete_related = False
        return formset


class ServicioDeCotizacionInlineAdmin(admin.TabularInline):
    model = ServicioDeCotizacion
    form = ServicioDeCotizacionForm
    max_num = 0

    def get_extra(self, request, obj=None, **kwargs):
        return 0

    def get_formset(self, request, obj=None, **kwargs):
        """
        Override the formset function in order to remove the add, change and remove buttons beside the foreign
        key pull-down menus in the inline.
        """
        formset = super(ServicioDeCotizacionInlineAdmin, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['servicio'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_delete_related = False
        return formset


class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('ver', 'fecha', 'solicitud')
    autocomplete_fields = ('solicitud',)
    actions = None
    form = CotizacionForm

    class Media:
        js = ('cotizacion.js', '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js')

    def ver(self, obj):
        html = '<a href="/admin/cotizaciones/cotizacion_detail/{}" class="icon-block"><i class="fa fa-eye"></i></a>'.format(obj.pk)
        return mark_safe(html)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        obj.save()

    def get_queryset(self, request):
        return Cotizacion.objects.filter(creado_por=request.user)

    def response_add(self, request, obj, **kwargs):
        if "_generar-items" in request.POST:
            obj.save()
            materiales_generados = MaterialDeCotizacion.objects.filter(cotizacion=obj)
            servicios_generados = ServicioDeCotizacion.objects.filter(cotizacion=obj)

            if materiales_generados or servicios_generados:
                self.message_user(request, "Los items de la cotización ya fueron creados")
            else:
                try:
                    filtro = 'm' if obj.solicitud.tipo == TiposDeCotizacion.MATERIAL else 's'
                    detalles_en_solicitud = [item for item in obj.solicitud.presupuesto.get_lista_de_recursos().items() if
                             item[0][0] == filtro]

                    tipo_de_items = 'Materiales'
                    if filtro == 'm':
                        for m in detalles_en_solicitud:
                            MaterialDeCotizacion.objects.create(cotizacion=obj, material_id=int(m[0][1:]))
                    elif filtro == 's':
                        tipo_de_items = 'Servicios'
                        for s in detalles_en_solicitud:
                            ServicioDeCotizacion.objects.create(cotizacion=obj, servicio_id=int(s[0][1:]))

                    self.message_user(request, f'{tipo_de_items} generados con éxito')
                except Exception as e:
                    self.message_user(request, "Error: %s" % str(e))
            return HttpResponseRedirect("/admin/cotizaciones/cotizacion/%s/change/" % obj.pk)
        return super().response_change(request, obj)

    def response_change(self, request, obj):
        if "_generar-items" in request.POST:
            materiales_generados = MaterialDeCotizacion.objects.filter(cotizacion=obj)
            servicios_generados = ServicioDeCotizacion.objects.filter(cotizacion=obj)

            if materiales_generados or servicios_generados:
                self.message_user(request, "Los items de la cotización ya fueron creados")
            else:
                try:
                    filtro = 'm' if obj.solicitud.tipo == TiposDeCotizacion.MATERIAL else 's'
                    detalles_en_solicitud = [item for item in obj.solicitud.presupuesto.get_lista_de_recursos().items()
                                             if
                                             item[0][0] == filtro]

                    tipo_de_items = 'Materiales'
                    if filtro == 'm':
                        for m in detalles_en_solicitud:
                            MaterialDeCotizacion.objects.create(cotizacion=obj, material_id=int(m[0][1:]))
                    elif filtro == 's':
                        tipo_de_items = 'Servicios'
                        for s in detalles_en_solicitud:
                            ServicioDeCotizacion.objects.create(cotizacion=obj, servicio_id=int(s[0][1:]))

                    self.message_user(request, f'{tipo_de_items} generados con éxito')
                except Exception as e:
                    self.message_user(request, "Error: %s" % str(e))
            return HttpResponseRedirect("/admin/cotizaciones/cotizacion/%s/change/" % obj.pk)
        return super().response_change(request, obj)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        cotizacion = Cotizacion.objects.get(id=object_id)
        if cotizacion.solicitud.tipo == TiposDeCotizacion.MATERIAL:
            self.inlines = (MaterialDeCotizacionInlineAdmin, )
        elif cotizacion.solicitud.tipo == TiposDeCotizacion.SERVICIOS:
            self.inlines = (ServicioDeCotizacionInlineAdmin, )
        return super(CotizacionAdmin, self).change_view(request, object_id, form_url, extra_context)


admin.site.register(Cotizacion, CotizacionAdmin)

