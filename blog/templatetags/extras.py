from atexit import register
from django import template
register=template.Library()

@register.filter(name='get_val')
def get_val(Dict,key):
    return Dict.get(key)

@register.filter(name='get_length')
def get_length(Dict,key):
    if key not in Dict:
        size=0
    else:
        size=len(Dict.get(key))
    return size

