from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'contact__form--input', 'placeholder': 'Ваше ім\'я'
    }))

    surname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'contact__form--input', 'placeholder': 'Ваше прізвище'
    }))

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'contact__form--input', 'placeholder': 'Ваша Email адреса'
    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__form--input', 'placeholder': 'Номер телефону +380ХХ ХХХ ХХ ХХ'
    }))

    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'contact__form--textarea', 'placeholder': 'Ваше повідомлення'
    }))

    class Meta:
        model = Contact
        fields = ('name', 'surname', 'email', 'phone', 'message')
