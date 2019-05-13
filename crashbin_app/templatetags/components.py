from django import template

register = template.Library()


@register.inclusion_tag('crashbin_app/bin_list_component.html')
def bin_list(bins, prefix=''):
    """Generate a list showing the given bin and its contents.

    If 'prefix' is given, it's prepended to HTML ids so that the component can
    be used multiple times on the same page without conflicting IDs.
    """
    return {'bins': bins, 'prefix': prefix}


@register.inclusion_tag('crashbin_app/report_list_component.html')
def report_list(reports, prefix=''):
    """Generate a list showing the given report and its contents.

    If 'prefix' is given, it's prepended to HTML ids so that the component can
    be used multiple times on the same page without conflicting IDs.
    """
    return {'reports': reports, 'prefix': prefix}


@register.inclusion_tag('crashbin_app/modal_delete_component.html')
def modal_delete(bin=None):
    return {'bin': bin}


@register.inclusion_tag('crashbin_app/search_component.html')
def search():
    """Generate a bin/report search box."""
    return {}
