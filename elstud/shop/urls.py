from django.urls import path

from .views import *
urlpatterns=[
    path('', ProductListView.as_view(), name='shop_index'),
    path('categories/<slug:cat_slug>/', categories),
    path('post/<slug:post_slug>/', show_post)
]

handler404 = pageNotFound