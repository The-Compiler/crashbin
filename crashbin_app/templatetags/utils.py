from django import template

from crashbin_app import utils
from crashbin_app.models import Label


register = template.Library()


@register.simple_tag
def custom_css() -> str:
    return utils.config.CUSTOM_CSS


@register.simple_tag
def label_style(label: Label) -> str:
    font_color = utils.font_color(*utils.parse_hex_color(label.color))
    return 'background-color: {} !important; color: {} !important;'.format(label.color, font_color)
