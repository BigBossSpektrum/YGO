from django import template

register = template.Library()

@register.filter
def to(value):
    return range(1, value + 1) if isinstance(value, int) and value > 0 else []

@register.filter
def split(value, delimiter):
    """Filtro para dividir una cadena por un delimitador."""
    return value.split(delimiter)