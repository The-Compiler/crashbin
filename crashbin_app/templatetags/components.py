import typing

from django import template

from crashbin_app.models import Bin, Report


register = template.Library()

_RenderData = typing.Dict[str, typing.Any]


@register.inclusion_tag("crashbin_app/bin_list_component.html")
def bin_list(bins: typing.Iterable[Bin], prefix: str = "") -> _RenderData:
    """Generate a list showing the given bin and its contents.

    If 'prefix' is given, it's prepended to HTML ids so that the component can
    be used multiple times on the same page without conflicting IDs.
    """
    return {"bins": bins, "prefix": prefix}


@register.inclusion_tag("crashbin_app/report_list_component.html")
def report_list(reports: typing.Iterable[Report], prefix: str = "") -> _RenderData:
    """Generate a list showing the given report and its contents.

    If 'prefix' is given, it's prepended to HTML ids so that the component can
    be used multiple times on the same page without conflicting IDs.
    """
    return {"reports": reports, "prefix": prefix}


@register.inclusion_tag("crashbin_app/modal_delete_component.html")
def modal_delete(what: str, bin_obj: Bin = None) -> _RenderData:
    return {"what": what, "bin": bin_obj}


@register.inclusion_tag("crashbin_app/search_component.html")
def search(path: str) -> _RenderData:
    """Generate a bin/report search box."""
    return {"path": path}
