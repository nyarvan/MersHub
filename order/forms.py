from django import forms
from .models import Order


class CreateOrderForm(forms.ModelForm):
    """
    Form class for creating orders.

    This form is used to collect information from users to create an order.

    Attributes:
        DELIVERY_METHOD (list of tuples): Choices for delivery methods.
        PAYMENT_METHOD (list of tuples): Choices for payment methods.
        delivery (ChoiceField): Field for selecting delivery method.
        payment (ChoiceField): Field for selecting payment method.

    """
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

    delivery = forms.ChoiceField(choices=DELIVERY_METHOD, widget=forms.Select(
        attrs={
                'class': 'checkout__input--select__field border-radius-5'
            }))

    payment = forms.ChoiceField(choices=PAYMENT_METHOD, widget=forms.Select(
        attrs={
                'class': 'checkout__input--select__field border-radius-5'
            }))

    class Meta:
        """
        Metadata class for the form.

        Attributes:
            model (Model): The model class representing the order.
            exclude (list): A list of fields to exclude from the form.
            widgets (dict): A dictionary containing custom widgets for
        form fields.

        """
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
                'class': 'checkout__input--field border-radius-5',
                'placeholder': '+38(066) 123 45 67'
            }),
            'email': forms.TextInput(attrs={
                'class': 'checkout__input--field border-radius-5',
                'placeholder': 'you@example.com'
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
