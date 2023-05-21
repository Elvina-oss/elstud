from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import F
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from shop.forms import ProductForm
from shop.models import *


def show_post(request, post_slug):
    post = get_object_or_404(Product, slug=post_slug)
    context = {
        'post': post,
        #    'menu' : menu,
        'title': post.name,
        'cat_selected': post.cat_id,
    }
    return render(request, 'post.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        context['tittle'] = 'Магазин'
        context['wishlist_products_id'], context['wishlist_quantity'] = self.get_wishlist_products_and_quantity()
        context['cart_products_id'], context['cart_quantity'] = self.get_cart_products_and_quantity()



        return context

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('productcategory_set__category')
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(productcategory__category__slug=category_slug)
        return queryset

    def get_wishlist_products_and_quantity(self):
        wishlist_product_ids = []
        user = self.request.user
        quantity = 0
        if user.is_authenticated:
            try:
                wishlist = Wishlist.objects.get(user=user)
                quantity = wishlist.quantity
                wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
                wishlist_product_ids = set(item.product_id for item in wishlist_items)
            except Wishlist.DoesNotExist:
                pass
        return wishlist_product_ids, quantity

    def get_cart_products_and_quantity(self):
        cart_product_ids = []
        user = self.request.user
        quantity = 0
        if user.is_authenticated:
            try:
                cart = Cart.objects.get(user=user)
                quantity = cart.quantity
                cart_items = CartItem.objects.filter(cart=cart)
                cart_product_ids = set(item.product_id for item in cart_items)
            except Cart.DoesNotExist:
                pass
        return cart_product_ids, quantity


@method_decorator(permission_required('shop.add_product'), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    success_url = reverse_lazy('shop_index')

    def form_valid(self, form):
        # Устанавливаем текущего пользователя как продавца товара
        form.instance.seller = UserProfile.objects.get(user=self.request.user)
        product = form.save()
        categories = form.cleaned_data['categories']
        for cat in categories:
            ProductCategory.objects.create(product=product, category=cat)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Добавить продукт'
        return context


class WishListView(ListView):
    model = WishlistItem
    template_name = 'wishlist.html'
    context_object_name = 'products'

    def get_queryset(self):
        wishlist = Wishlist.objects.get_or_create(user=self.request.user)[0]
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
        product_ids = wishlist_items.values_list('product_id', flat=True)
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Избранное'
        return context

@csrf_exempt
def add_to_wishlist(request):
    if request.method == 'POST' and 'product_slug' in request.POST:
        product_slug = request.POST['product_slug']
        product = get_object_or_404(Product, slug=product_slug)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
        # wishlist.quantity = F('quantity') + 1
        wishlist.quantity = WishlistItem.objects.filter(wishlist=wishlist).count()
        wishlist.save()
        wishlist_quantity = wishlist.quantity
        return JsonResponse({'success': True, 'wishlist_quantity': wishlist_quantity})
    else:
        return JsonResponse({'success': False})


@csrf_exempt
def delete_from_wishlist(request):
    if request.method == 'POST' and 'product_slug' in request.POST:
        product_slug = request.POST['product_slug']
        product = get_object_or_404(Product, slug=product_slug)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_item = get_object_or_404(WishlistItem, product=product.id, wishlist=wishlist.id)
        wishlist_item.delete()
        # wishlist.quantity = F('quantity') - 1
        wishlist.quantity = WishlistItem.objects.filter(wishlist=wishlist).count()
        wishlist.save()
        wishlist_quantity = wishlist.quantity
        return JsonResponse({'success': True, 'wishlist_quantity': str(wishlist_quantity)})
    else:
        return JsonResponse({'success': False})



class CartView(ListView):
    model = CartItem
    template_name = 'cart.html'
    context_object_name = 'products'

    def get_queryset(self):
        cart = Cart.objects.get_or_create(user=self.request.user)[0]
        cart_items = CartItem.objects.filter(cart=cart)
        product_ids = cart_items.values_list('product_id', flat=True)
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Корзина'
        return context

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST' and 'product_slug' in request.POST:
        product_slug = request.POST['product_slug']
        product = get_object_or_404(Product, slug=product_slug)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        # cart.quantity = F('quantity') + 1
        cart.quantity = CartItem.objects.filter(cart=   cart).count()
        cart.save()
        cart_quantity = cart.quantity
        return JsonResponse({'success': True, 'cart_quantity':cart_quantity})
    else:
        return JsonResponse({'success': False})


@csrf_exempt
def delete_from_cart(request):
    if request.method == 'POST' and 'product_slug' in request.POST:
        product_slug = request.POST['product_slug']
        product = get_object_or_404(Product, slug=product_slug)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, product=product.id, cart=cart.id)
        cart_item.delete()
        # cart.quantity = F('quantity') - 1
        cart.quantity = CartItem.objects.filter(cart=cart).count()
        cart.save()
        cart_quantity = cart.quantity
        return JsonResponse({'success': True, 'cart_quantity': str(cart_quantity)})
    else:
        return JsonResponse({'success': False})
