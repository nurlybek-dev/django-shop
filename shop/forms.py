from django import forms
from django.forms import HiddenInput
from django.http import request
from shop.models import Order, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'user', 'rating', 'comment']
        widgets = {
            'product': HiddenInput(),
            'user': HiddenInput()
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'contact_phone']
