from django import template

from crashbin_app import utils
from crashbin_app.models import Label


register = template.Library()


@register.simple_tag
def custom_css() -> str:
    return utils.config.CUSTOM_CSS


@register.simple_tag
def label_style(label: Label) -> str:
    font_color = utils.Color.from_hex(label.color).font_color()
    return "background-color: {}; color: {};".format(label.color, font_color)


@register.simple_tag(takes_context=True)
def active_class(context, name) -> str:
    path = context["request"].path

    conditions = [
        name == "home" and path == "/",
        name == "bins" and path == "/bins",
        name == "bins" and path.startswith("/bin/"),
        name == "reports" and path == "/reports",
        name == "reports" and path.startswith("/report/"),
        name == "labels" and path == "/labels",
        name == "labels" and path.startswith("/label/"),
    ]
    return "active" if any(conditions) else ""
