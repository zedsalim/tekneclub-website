# forms.py
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['name'].initial = user.first_name.capitalize() + ' ' + user.last_name.capitalize()
            self.fields['email'].initial = user.email


class ReplyMessageForm(forms.ModelForm):
    content = forms.CharField(
        max_length=1500,
        required=True,
        widget=forms.Textarea(attrs={'class': 'bg-gray-800 appearance-none border border-gray-700 rounded w-full py-2 px-4 text-white', 'placeholder': 'Your message', 'autofocus': True})
    )
    
    class Meta:
        model = Reply
        fields = ["content"]


class FeedBackForm(forms.ModelForm):
    fbk_name = forms.CharField(
        max_length=100,
        required=True,
        label='Name',
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-800 appearance-none border border-gray-700 rounded w-full py-2 px-4 text-white', 
            'placeholder': 'Complete Name', 
            'autofocus': False
        })
    )
    fbk_content = forms.CharField(
        max_length=1000,
        required=True,
        label='Content',
        widget=forms.Textarea(attrs={
            'class': 'bg-gray-800 appearance-none border border-gray-700 rounded w-full py-2 px-4 text-white', 
            'placeholder': 'Your feedback', 
            'autofocus': False, 
            'rows': 5
        })
    )

    class Meta:
        model = FeedBack
        fields = ["fbk_name", "fbk_content"]


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['fbk_name'].initial = user.first_name.capitalize() + ' ' + user.last_name.capitalize()
