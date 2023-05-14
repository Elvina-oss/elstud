from django import forms

from shop.models import *


class ProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Категории'
    )

    class Meta:
        model = Product
        fields = ['name', 'content', 'photo', 'price', 'categories']