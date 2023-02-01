from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product

# Create your views here.


def all_products(request):
    ''' A view to show all products, including sorting and searching '''

    products = Product.objects.all()
    query = None  # To start page without an error that no search term has been entered

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)  # Used to query on OR basis, i before contains makes them case insenstive
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,

    }

    return render(request, 'products/products.html', context)  # context added as will need to send some things back to the template


def product_detail(request, product_id):
    ''' A view to show individual product details '''

    products = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
