from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def media_path(string):
    str_template = "/img/{}".format(string)
    return mark_safe(f"{str_template}")