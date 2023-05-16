from django.urls import path

from .views import *
urlpatterns = [
    path('products/', ProductListView.as_view(), name='shop_index'),
    path('products/<slug:category_slug>/', ProductListView.as_view(), name='shop_index_by_category'),
    path('post/<slug:post_slug>/', show_post),
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('add_to_wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('delete_from_wishlist/', delete_from_wishlist, name='delete_from_wishlist'),
    path('wishlist/', WishListView.as_view(), name='wishlist'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('delete_from_cart/', delete_from_cart, name='delete_from_cart'),
    path('cart/', CartView.as_view(), name='cart')
]

handler404 = pageNotFound