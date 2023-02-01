from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


def all_products(request):
    ''' A view to show all products, including sorting and searching '''

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)  # context added as will need to send some things back to the template


def product_detail(request, product_id):
    ''' A view to show individual product details '''

    products = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
