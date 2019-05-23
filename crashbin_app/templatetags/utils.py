from django import template

from crashbin_app import utils
from crashbin_app.models import Label


register = template.Library()


@register.simple_tag
def custom_css() -> str:
    return utils.config.CUSTOM_CSS


@register.simple_tag
def label_style(label: Label) -> str:
    return 'background-color: {} !important; color: white !important;'.format(label.color)
