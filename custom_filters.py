# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='split_string')
def split_string(value, delimiter=','):
    return value.split(delimiter)