from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404


# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from shop.forms import ProductForm
from shop.models import *




def show_post(request, post_slug):
    post = get_object_or_404(Product, slug=post_slug)
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
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        context['tittle'] = 'Магазин'
        return context

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('productcategory_set__category')
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(productcategory__category__slug=category_slug)

        return queryset


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
        print(context)
        return context
