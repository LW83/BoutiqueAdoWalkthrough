from django.contrib import admin
from .models import Order, OrderLineItem


# Inline items allows edit and add line items in the admin from inside order model
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag',
                       'stripe_pid',)

    # Allows us to specify order of fields in Admin interface
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city',
              'street_address1', 'street_address2',
              'county', 'delivery_cost', 'order_total',
              'grand_total', 'original_bag', 'stripe_pid',)

    # To restrict columns that show up in the order list
    list_display = ('order_number', 'date', 'full_name',
                    'delivery_cost', 'order_total',
                    'grand_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
