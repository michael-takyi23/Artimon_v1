from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from products.models import Product

# Create your views here.
def view_cart(request):
    """ A view that renders the shopping cart content page """

    return render(request, 'cart/cart.html')

def add_to_cart(request, item_id):
    """ A view to add a quantity of a product to the shopping cart """
    
    product = get_object_or_404(Product, pk=item_id) 
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    size = request.POST.get('product_size') if 'product_size' in request.POST else None

    if size:
        # Handle products with sizes
        if item_id in cart:
            if 'items_by_size' in cart[item_id] and size in cart[item_id]['items_by_size']:
                cart[item_id]['items_by_size'][size] += quantity
            else:
                if 'items_by_size' not in cart[item_id]:
                    cart[item_id]['items_by_size'] = {}
                cart[item_id]['items_by_size'][size] = quantity
        else:
            cart[item_id] = {'items_by_size': {size: quantity}}
    else:
        # Handle products without sizes
        if item_id in cart:
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity

    # Save the updated cart to the session
    request.session['cart'] = cart
    messages.success(request, f'Added {product.name} to your cart!')
    return redirect(redirect_url)
    
def remove_from_cart(request, item_id):
    """ A view to remove an item from the shopping cart """
    
    try:  
        size = None 
        if 'product_size' in request.POST:
            size = request.POST['product_size'] 
        cart = request.session.get('cart', {}) 

        
        if size:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:  # Remove the item completely if no sizes are left
               cart.pop(item_id)
        else:
            cart.pop(item_id)

            request.session['cart'] = cart
            messages.success(request, 'Item removed from your cart!')
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)

def confirm_order(request):
    """ A view to confirm the order """
    # Order confirmation logic goes here

    # Clear the cart after order confirmation
    request.session['cart'] = {}
    messages.success(request, 'Order confirmed successfully!')
    return redirect('order_confirmation_page')