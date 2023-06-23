from django import template
from django.template.defaultfilters import stringfilter

from markdown2 import Markdown

register = template.Library()
md = Markdown()


@register.filter()
@stringfilter
def markdown(value):
    return md.convert(value)
