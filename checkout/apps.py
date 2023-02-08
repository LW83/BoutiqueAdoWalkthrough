from django.apps import AppConfig


# To let django know there is a new signals module with listeners
class CheckoutConfig(AppConfig):
    name = 'checkout'

    def ready(self):
        import checkout.signals

# Now everytime a line item is saved or deleted custom update total
# model method will be called updating order totals automatically
