from .models import Post
from .models import Comment

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


class CommentCreateForm(ModelForm):
    """
    Форма создания коммента к посту
    """
    text = forms.CharField(label='',
                           min_length=12,
                           max_length=128,
                           widget=forms.Textarea(attrs={
                               'class': 'form-control',
                               'placeholder': 'Your comment here',
                               'rows': '3',
                           }))

    class Meta:
        model = Comment
        fields = ['text']
