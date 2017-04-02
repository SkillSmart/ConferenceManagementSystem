from django import template

register = template.Library()

# This is an introductive example how to create my own template tags in django
@register.filter(is_safe=True)
def publisher_list(publisher):
    # Be sure to check if the input is safe before returning !!!
    if publisher == 'Packt':
        return '%s (https://www.packtpub.com/)' % publisher
    else:
        return publisher
    # Use it like this: {{book.publisher|publisher_link}}

# Example to creat one that accepts additional arguments
@register.filter(is_safe=True)
def youtube_embed(url, hd=False):
    # Be sure to check if the input is safe before returning !!!
    if hd:
        return get_youtube_hd_embed(url)
    else:
        return get_youtube_embed(url)
    # Use it like this: {{youtube_link|youtube_embed:"True"}}


# then load the filters: {% load filters %}