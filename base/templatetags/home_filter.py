from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='count_worlds')
@stringfilter
def count_worlds(string):
    return len(string.split(' '))
