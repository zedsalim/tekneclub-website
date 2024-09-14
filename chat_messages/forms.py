from django import forms
from .models import *


class ContactUsForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'bg-gray-800 appearance-none border border-gray-700 rounded w-full py-2 px-4 text-white', 'placeholder': 'Complete Name', 'autofocus': False})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'bg-gray-800 appearance-none border border-gray-700 rounded w-full py-2 px-4 text-white', 'placeholder': 'Email', 'autofocus': False})
    )
    subject = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'bg-gray-800 appearance-none border border-gray-700 rounded w-full py-2 px-4 text-white', 'placeholder': 'Your subject', 'autofocus': False})
    )
    content = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.Textarea(attrs={'class': 'bg-gray-800 appearance-none border border-gray-700 rounded w-full py-2 px-4 text-white', 'placeholder': 'Your message', 'autofocus': False})
    )

    class Meta:
              model = Message
              fields = ["name", "email", "subject", "content"]