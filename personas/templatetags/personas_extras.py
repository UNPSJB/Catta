from django.template.defaulttags import register
from django import template

register = template.Library()

@register.filter
def totalizar(queryset):
    precio_total = 0
    for servicio in queryset:
        precio_total += servicio.precio
    return precio_total

