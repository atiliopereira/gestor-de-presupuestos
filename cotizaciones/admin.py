from django.contrib import admin
from django.utils.safestring import mark_safe

from cotizaciones.constants import EstadoDeSolicitud
from cotizaciones.forms import SolicitudSearchForm, SolicitudForm, MaterialDeSolicitudForm, \
    ServicioDeSolicitudForm
from cotizaciones.models import Solicitud, MaterialDeSolicitud, ServicioDeSolicitud
from cotizaciones.views import get_solicitudes_queryset


class MaterialDeSolicitudInline(admin.TabularInline):
    model = MaterialDeSolicitud
    form = MaterialDeSolicitudForm
    autocomplete_fields = ('material',)

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1

    def get_formset(self, request, obj=None, **kwargs):
        """
        Override the formset function in order to remove the add, change and remove buttons beside the foreign
        key pull-down menus in the inline.
        """
        formset = super(MaterialDeSolicitudInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['material'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_delete_related = False
        return formset


class ServicioDeSolicitudInline(admin.TabularInline):
    model = ServicioDeSolicitud
    form = ServicioDeSolicitudForm
    autocomplete_fields = ('servicio',)

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1

    def get_formset(self, request, obj=None, **kwargs):
        """
        Override the formset function in order to remove the add, change and remove buttons beside the foreign
        key pull-down menus in the inline.
        """
        formset = super(ServicioDeSolicitudInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['servicio'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_delete_related = False
        return formset


class SolicitudAdmin(admin.ModelAdmin):
    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js', 'solicitud.js',)
    list_display = ('ver', 'id', 'fecha', 'vencimiento', 'tipo', 'estado', 'concretar', 'cancelar')
    form = SolicitudForm
    inlines = (MaterialDeSolicitudInline, ServicioDeSolicitudInline)
    actions = None

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        obj.save()

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

