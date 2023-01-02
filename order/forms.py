from django import forms
from .models import Order


class CreateOrderForm(forms.ModelForm):
    DELIVERY_METHOD = [
        ('Самовывоз', 'Самовивозом'),
        ('Новой почтой', 'Доставка Новою почтою'),
        ('Доставка', 'Доставка MERSHUB')
    ]

    PAYMENT_METHOD = [
        ('Наличными', 'Оплата готівкою'),
        ('Картой', 'Оплата картою'),
        ('Наложенный платеж', 'Накладеним платежем')
    ]

    delivery = forms.ChoiceField(choices=DELIVERY_METHOD, widget=forms.Select(attrs={
                'class': 'checkout__input--select__field border-radius-5'
            }))

    payment = forms.ChoiceField(choices=PAYMENT_METHOD, widget=forms.Select(attrs={
                'class': 'checkout__input--select__field border-radius-5'
            }))

    class Meta:
        model = Order
        exclude = ['created', 'updated', 'paid']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'checkout__input--field border-radius-5'
            }),
            'surname': forms.TextInput(attrs={
                'class': 'checkout__input--field border-radius-5'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'checkout__input--field border-radius-5', 'placeholder': '+38(066) 123 45 67'
            }),
            'email': forms.TextInput(attrs={
                'class': 'checkout__input--field border-radius-5', 'placeholder': 'you@example.com'
            }),
            'country': forms.TextInput(attrs={
                'class': 'checkout__input--field border-radius-5'
            }),
            'city': forms.TextInput(attrs={
                'class': 'checkout__input--field border-radius-5'
            }),
            'address': forms.TextInput(attrs={
                'class': 'checkout__input--field border-radius-5'
            }),
            'post': forms.TextInput(attrs={
                'class': 'checkout__input--field border-radius-5'
            })
        }
