from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    ''' A view that renders the bag contents page '''

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))  # Convert to integer as will come from template as a string
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {}) # Storing in session allows in to stay in bag while browsing until leaving sites. Checking if bag variable in session and if not creates one

    if item_id in list(bag.keys()):
        bag[item_id] += quantity  # If the item is already in the bag, increase the quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag # Then overwriting item in the session with updated version 
    # print(request.session['bag']) - commented out as was only included to test items were being added to the bag
    return redirect(redirect_url)
