from django import forms
from .models import Post

class AddPostForm(forms.ModelForm):
    class Meta:
            model = Post
            fields = ["title", "content", "categories", "status"]
            widgets = {
                'title': forms.TextInput(attrs={
                    'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white',
                    'placeholder': 'Post Title',
                    'autofocus': True
                }),
                'content': forms.Textarea(attrs={
                    'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white',
                    'placeholder': 'Content',
                    'rows': 15,
                }),
                'status': forms.Select(attrs={
                    'class': 'bg-gray-700 border border-green-600 rounded w-full py-2 px-4 text-white'
                }),
                'categories': forms.CheckboxSelectMultiple(attrs={
                    'class': 'bg-gray-700 border-gray-600 text-white text-left px-3 interests-scrollable'
                }),
            }