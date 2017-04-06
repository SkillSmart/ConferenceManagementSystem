from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''

# from django.template.defaulttags import register
# ...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def check_available(value):
    if value == 0:
        return 'fa-exit success'
    else:
        return 'fa-check danger'
