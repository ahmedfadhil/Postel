from urllib import quote_plus
from django import template

register = template.library()

@register.filter
def urlify(value):
    return quote_plus(value)
