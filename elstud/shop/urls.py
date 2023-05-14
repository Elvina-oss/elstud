from django.urls import path

from .views import *
urlpatterns=[
    path('products/', ProductListView.as_view(), name='shop_index'),
    path('products/<slug:category_slug>/', ProductListView.as_view(), name='shop_index_by_category'),
    path('post/<slug:post_slug>/', show_post),
    path('product_create/', ProductCreateView.as_view(), name='product_create')
]

handler404 = pageNotFound