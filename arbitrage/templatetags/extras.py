from django import template

register = template.Library()

@register.filter
def getRatio(value, exchanges):
    return value.getRatio(exchanges)