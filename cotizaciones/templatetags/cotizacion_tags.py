from __future__ import unicode_literals
from django import template

from presupuestos.templatetags.presupuesto_tags import advanced_search_form

register = template.Library()


@register.inclusion_tag('admin/cotizaciones/solicitud/solicitud_search_form.html', takes_context=True)
def solicitud_search_form(context, cl):
    return advanced_search_form(context, cl)
