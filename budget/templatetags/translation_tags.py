from django import template
from django.utils.translation import gettext

register = template.Library()

@register.filter
def translate(value):
    return gettext(str(value))
