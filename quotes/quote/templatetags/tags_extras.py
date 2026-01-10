from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter('load_tags')
def load_tags(value):
    links = []
    for item in value.all():
        url = reverse('quote:tags_quotes', args=(item.id,))
        links.append(f'<a href="{url}" style="border-radius: 5px;">{item.name}</a>')
    return mark_safe(', '.join(links))


@register.filter('tag_name_capitalize')
def capitalize_tag_name(value):
    return str(value).capitalize()
