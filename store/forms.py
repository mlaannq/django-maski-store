from django import forms
from .models import CartItem

class CartUpdateForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'min': 1,
                'class': 'form-control'
            })
        }

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        label='Адрес доставки',
        widget=forms.Textarea(attrs={'rows': 3})
    )
    email = forms.EmailField(label='Email для чека')
    phone = forms.CharField(label='Контактный телефон')