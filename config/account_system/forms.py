from django import forms
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from django.template.defaultfilters import capfirst
from friendship.models import FriendshipRequest

from .models import Account

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField, UserModel, SetPasswordForm, \
    PasswordChangeForm


class AccountLoginForm(forms.Form):
    """
    Форма для входа
    """
    username = UsernameField(widget=forms.TextInput(attrs={
        'class': 'fadeIn second',
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'fadeIn second',
        'placeholder': 'Password',

    }))
    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': "This account is inactive.",
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields['username'].max_length = username_max_length
        self.fields['username'].widget.attrs['maxlength'] = username_max_length
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )


class AccountEditForm(UserChangeForm):
    """
    Форма для редактирования аккаунта пользователя
    """
    first_name = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={
                                     'class': 'fadeIn second',
                                     'placeholder': 'First name',
                                 }))
    last_name = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'fadeIn second',
                                    'placeholder': 'Last name',
                                }))
    about_me = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={
                                   'class': 'fadeIn second',
                                   'placeholder': 'About me',
                               }))
    location = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={
                                   'class': 'fadeIn second',
                                   'placeholder': 'Location',
                               }))
    avatar = forms.ImageField(required=False,
                              widget=forms.FileInput(attrs={
                                  'class': 'fadeIn second',
                                  'placeholder': 'Avatar',
                              }))

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'about_me', 'location', 'avatar')


class AccountCreateForm(UserCreationForm):
    """
    """
    password1 = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'fadeIn second',
            'placeholder': 'Password',
        }))
    password2 = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'fadeIn second',
            'placeholder': 'Repeat password',
        }))
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'fadeIn second',
            'placeholder': 'Username',
        }))
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'fadeIn second',
            'placeholder': 'Email',
        }))

    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class FriendsSearchForm(forms.Form):
    """
    Форма для поиска друзей
    """
    username = forms.CharField(required=False, label='',
                               widget=forms.TextInput(attrs={
                                   'class': 'fadeIn second',
                                   'placeholder': 'Username',
                               }))


class AccountChangePasswordForm(PasswordChangeForm):
    """
    Форма смены пароля
    """
    old_password = forms.CharField(label='',
                                   widget=forms.TextInput(attrs={'class': 'fadeIn second',
                                                                 'placeholder': 'Old password',
                                                                 }))
    new_password1 = forms.CharField(label='',
                                    widget=forms.TextInput(attrs={'autocomplete': 'new-password',
                                                                  'class': 'fadeIn second',
                                                                  'placeholder': 'New password',
                                                                  }))
    new_password2 = forms.CharField(label='',

                                    widget=forms.TextInput(attrs={'autocomplete': 'new-password',
                                                                  'class': 'fadeIn second',
                                                                  'placeholder': 'New password repeat',
                                                                  }))
    error_messages = {
        'password_incorrect': "Your old password was entered incorrectly. Please enter it again.",
        'password_mismatch': 'The two password fields didn’t match.',

    }
