from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.


def all_products(request):
    ''' A view to show all products, including sorting and searching '''

    products = Product.objects.all()
    query = None  # To start page without an error that no search term has been entered
    categories = None
    sort = None # Need to ensure defined in order to return template properly when not using any sorting. 
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name' # __ allows drilling into related model
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')  # if it exists splitting into list at the comma
            products = products.filter(category__name__in=categories)  # doubleunderscore syntax used her means looking for name field of category model can do here as category and product model linked by FK
            categories = Category.objects.filter(name__in=categories)  # converting the list of strings of category names into a list of actual category objects so can access their fields in the template

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)  # Used to query on OR basis, i before contains makes them case insenstive
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)  # context added as will need to send some things back to the template


def product_detail(request, product_id):
    ''' A view to show individual product details '''

    products = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
