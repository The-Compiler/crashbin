from django import template

from crashbin_app import utils


register = template.Library()


@register.simple_tag
def custom_css():
    return utils.config.CUSTOM_CSS
