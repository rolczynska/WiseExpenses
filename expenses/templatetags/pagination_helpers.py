from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def remove_page_param(context):
    request = context['request']
    query_params = request.GET.copy()
    query_params.pop('page', None)
    return query_params.urlencode()
