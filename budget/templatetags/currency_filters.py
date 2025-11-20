from django import template

register = template.Library()

@register.filter
def currency_format(value, currency_symbol='¥'):
    """Format amount with currency symbol"""
    try:
        return f"{currency_symbol}{float(value):,.0f}"
    except (ValueError, TypeError):
        return f"{currency_symbol}0"