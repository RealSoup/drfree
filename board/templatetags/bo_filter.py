from django import template
import os

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def basename(value):
    if not value:
        return ''
    return os.path.basename(value)

@register.filter
def multiply(value, arg):
    return int(value) * int(arg)