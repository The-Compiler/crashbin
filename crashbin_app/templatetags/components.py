from django import template

register = template.Library()


@register.inclusion_tag('crashbin_app/bin_list_component.html')
def bin_list(bins, prefix=''):
    """Generate a list showing the given bin and its contents.

    If 'prefix' is given, it's prepended to HTML ids so that the component can
    be used multiple times on the same page without conflicting IDs.
    """
    return {'bins': bins, 'prefix': prefix}
