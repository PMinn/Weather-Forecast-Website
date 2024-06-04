from django import forms
from .models import UserProfile
from .counties import counties


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': '請輸入使用者名稱',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '請輸入密碼',
                'class': 'form-control'
            }
        )
    )


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': '請輸入使用者名稱',
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': '請輸入電子郵件',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '請輸入密碼',
                'class': 'form-control'
            }
        )
    )


class UpdateUserProfileForm(forms.Form):
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': '請輸入使用者名稱',
                'class': 'form-control'
            }
        ),
        required=False
    )
    defaultCounty = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.Select(
            choices=map(lambda x: (x, x), counties),
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '請輸入密碼',
                'class': 'form-control'
            }
        ),
        required=False
    )
    password_confirm = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '請再次輸入密碼',
                'class': 'form-control'
            }
        ),
        required=False
    )
