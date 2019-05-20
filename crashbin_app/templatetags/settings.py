from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def custom_css():
    return settings.CRASHBIN_CONFIG.CUSTOM_CSS
