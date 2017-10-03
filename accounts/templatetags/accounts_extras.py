from django import template

import markdown2

register = template.Library()

status = [
    "new", "accepted", "rejected"
]


@register.inclusion_tag('accounts/status_nav.html')
def status_app_list():
    return {'status': status}


@register.filter('markdown_to_html')
def markdown_to_html(markdown_text):
    """Converts markdown text to HTML"""
    html_body = markdown2.markdown(markdown_text)
    return html_body
