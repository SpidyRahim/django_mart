from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from django.core.paginator import Paginator

# Create your views here.


def stores(request, category_slug=None):
    # category = None
    # products = None na dileo cholbe karon python e by default access kora jay

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True, category=category)
        page = request.GET.get('page')
        paginator = Paginator(products, 3)

        paged_products = paginator.get_page(page)

    else:
        products = Product.objects.filter(is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')

        paged_products = paginator.get_page(page)

        for i in paged_products:
            print(i)

    categories = Category.objects.all()
    # print(category)

    context = {'products': paged_products, 'categories': categories}

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    single_product = Product.objects.get(
        slug=product_slug, category__slug=category_slug)
    return render(request, 'store/product-detail.html', {'product': single_product})
