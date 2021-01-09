from .models import Post

from django.forms import ModelForm
from django import forms


class PostCreateForm(ModelForm):
    """
    Создание поста
    """

    title = forms.CharField(label='',
                            min_length=12,
                            max_length=64,
                            widget=forms.TextInput(attrs={
                                'class': 'fadeIn second',
                                'placeholder': 'Title',
                            }))

    text = forms.CharField(label='',
                           min_length=32,
                           widget=forms.TextInput(attrs={
                               'class': 'fadeIn second',
                               'placeholder': 'Text',

                           }))

    class Meta:
        model = Post
        exclude = ['owner']
