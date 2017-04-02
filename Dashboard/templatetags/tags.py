from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Great for simple tags
@register.simple_tag
def bootstrap_css():
    tags = [
        '<put the link to the bootstrap css cdn here.....',
        '<put the link to the bootstrap js cdn here.....'
    ]
    return ''.join(tags)

# 
@register.inclusion_tag('bootstrap_button.html')
def bootstrap_button(text, style='default'):
    return {
        'style': style.lower(),
        'text': text,
    }