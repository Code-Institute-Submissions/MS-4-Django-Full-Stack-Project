"""
Shop app views
    1. A view to the shop page
        With a query and sorting functions
    2. A view to the shop individual item page
        Filter query to return reladed by style products
"""


from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Product, Category


# Create your views here.
def shop(request):
    """A view to return the shop page
    Queries by product category, style
    Product sort functionality name, price
    ascending order or descending order
    """
    products = Product.objects.all()
    style_list = products.values('style').distinct()
    categories = Category.objects.all()
    category = 'all'
    sort_name = None
    sortkey = None
    style = 'all'
    query = 'None'
    shop = True
    if request.GET:
        if 'search' in request.GET:
            query = request.GET['search']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('shop'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
        if 'category' in request.GET:
            # Query products By category
            category = request.GET['category']
            if category == 'sale':
                products = products.filter(sale=True)
            elif category == 'all':
                products = products.all()
            else:
                products = products.filter(category__name=category)
        if 'style' in request.GET:
            # Query products by Style
            style = request.GET['style']
            if style != 'all':
                products = products.filter(style=style)
        if 'sort' in request.GET:
            # Sort By name, price, rating. Sorting
            # by descending and ascending order
            sortkey = request.GET['sort']
            if sortkey == 'name_asc':
                sort_name = 'Name (A-Z)'
                products = products.order_by('name')
            elif sortkey == 'name_desc':
                sort_name = 'Name (Z-A)'
                products = products.order_by('-name')
            elif sortkey == 'price_asc':
                sort_name = 'Price (L-H)'
                products = products.order_by('price')
            elif sortkey == 'price_desc':
                sort_name = 'Price (H-L)'
                products = products.order_by('-price')

    context = {
        'style_list': style_list,
        'categories': categories,
        'sort_name': sort_name,
        'products': products,
        'sortkey': sortkey,
        'cat': category,
        'style': style,
        'shop': shop,
    }
    return render(request, 'shop/shop.html', context)


# Create your views here.
def shop_item(request, item_id):
    """A view to return the shop item detailed page"""
    item = get_object_or_404(Product, pk=item_id)
    related = Product.objects.filter(style=item.style)
    context = {
        'item': item,
        'related': related,
    }
    return render(request, 'shop/shop_item.html', context)
