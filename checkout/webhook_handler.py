from django.http import HttpResponse

class StripeWH_Handler:
    """ Handle Stripe Webhooks"""

    def __init__(self, request):  # The init methos of the class is the setup method thats called every time an instance of the class is created
        self.request = request  # we're going to use it to assign the request as an attribute of the class

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
