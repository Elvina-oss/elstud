from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404


# Create your views here.
from django.views.generic import ListView

from shop.models import *


# def index(request):
#     return render(request, 'map.html')


def categories(request, catid):
    return HttpResponse(f"<h1>Это категории...</h1><p>{catid}</p>")

def show_post(request, post_slug):
    post = get_object_or_404(Product, slug = post_slug)
    context = {
        'post' : post,
    #    'menu' : menu,
        'title' : post.name,
        'cat_selected' : post.cat_id,
    }
    return render(request, 'post.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'map.html'

    def get_queryset(self):
        return Product.objects.prefetch_related('productcategory_set__category')
