from django import forms


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
