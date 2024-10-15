from django import forms
from django.forms import widgets,fields

from .models import Product,Check

class OrderForm(forms.Form):

    name=forms.CharField(widget=forms.Select(choices=[(p.id,p.name) for p in Product.objects.all()],attrs={'class': 'form-control', 'empty_value': True}))
    count=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'empty_value': True}))

class CheckForm(forms.ModelForm):

    class Meta:
        model=Check
        fields=['printer_id','type','status','order']
        widgets= {
            'status':forms.Select(attrs={'class': 'form-control', 'empty_value': True}),
            'type':forms.Select(attrs={'class': 'form-control', 'empty_value': True}),
            'printer_id': forms.Select(attrs={'class': 'form-control', 'empty_value': True}),
            'order':forms.TextInput(attrs={'class': 'form-control', 'empty_value': True})

        }
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','price','in_stock']
        widgets={
            'name':forms.TextInput(attrs={'class': 'form-control', 'empty_value': True}),
            'price':forms.NumberInput(attrs={'class': 'form-control', 'empty_value': True}),
            'in_stock':forms.NumberInput(attrs={'class': 'form-control', 'empty_value': True})
        }