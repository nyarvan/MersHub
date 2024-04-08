from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Form class for handling contact information.

    This form class defines fields for capturing contact information from
    users, such as their name, surname, email, phone number, and message.
    It also specifies validation rules and widget attributes for each field.

    Attributes:
        name (CharField): A field for capturing the user's name.
        surname (CharField): A field for capturing the user's surname.
        email (EmailField): A field for capturing the user's email address.
        phone (CharField): A field for capturing the user's phone number.
        message (CharField): A field for capturing the user's message.
        Meta (class): Inner class containing metadata for the form.
            model (Model): The model class associated with the form.
            fields (tuple): A tuple of field names to include in the form.

    """
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
        'class': 'contact__form--input', 'placeholder': 'Ваш номер телефону'
    }))

    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'contact__form--textarea', 'placeholder': 'Ваше повідомлення'
    }))

    class Meta:
        """
        A form for capturing contact information.

        This form is used to capture contact information submitted by users.

        Meta:
            model (Contact): The model class associated with this form.
            fields (tuple): The fields to be included in the form.

        """
        model = Contact
        fields = ('name', 'surname', 'email', 'phone', 'message')
