from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.


def view_bag(request):
    ''' A view that renders the bag contents page '''

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)  # Instead of Products.object.get in case product isnt found
    quantity = int(request.POST.get('quantity'))  # Convert to integer as will come from template as a string
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST('product_size')

    bag = request.session.get('bag', {}) # Storing in session allows in to stay in bag while browsing until leaving sites. Checking if bag variable in session and if not creates one

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity # If same id and same size
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id][items_by_size][size]} to your bag')
            else:
                bag[item_id]['items_by_size'][size] = quantity # Or if same id but different size
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}} # If item not already in bag, adding it as dictionary. May have multiple items with id but different sizes.
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity  # If the item is already in the bag, increase the quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag  # Then overwriting item in the session with updated version 
    # print(request.session['bag']) - commented out as was only included to test items were being added to the bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST('product_size')

    bag = request.session.get('bag', {}) 
    
    if size:
        if quantity > 0:
            bag[item_id]['item_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id][items_by_size][size]} to your bag')
        else:
            del bag[item_id]['item_by_size'][size]
            if not bag[item_id]['items_by_size']:  # If thats the only size they had then can remove entire item_id
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST('product_size')

        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['item_by_size'][size]  # If user is removing something with sizes want to only remove that specific size
            if not bag[item_id]['items_by_size']:  # If thats the only size they had then can remove entire item_id 
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HTTPResponse(status=200)  # Instead of returning redirect want to return a 200 HTTP response implying item successfully removed
   
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HTTPResponse(status=500)
