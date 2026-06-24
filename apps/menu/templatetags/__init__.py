from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Sözlükten anahtar ile değer al: {{ my_dict|get_item:key }}"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''
