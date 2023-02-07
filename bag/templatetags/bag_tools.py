from django import template


register = template.Library()


@register.filter(name='calc_subtotal')  # to register function as a template filter
def calc_subtotal(price, quantity):
    return price * quantity

# See django documentation for creating custom template tags and filters
