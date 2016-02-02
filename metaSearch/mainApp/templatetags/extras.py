from django import template

register = template.Library()

@register.filter
def is_required(value):
    if value.field.required:
        return 'required'
    return ''