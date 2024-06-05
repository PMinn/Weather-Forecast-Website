from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib import auth
from .forms import LoginForm, SignupForm, UpdateUserProfileForm
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms

# Create your views here.


def login(request):
    if request.method == 'GET':
        login_form = LoginForm()
        context = {
            'user': request.user,
            'login_form': login_form,
        }
        return render(request, 'login.html', context)
    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        context = {}
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                context['err_login_msg'] = '登入失敗，請檢查帳號密碼'
        else:
            context['err_login_msg'] = '登入失敗，請檢查帳號密碼'

        context['login_form'] = login_form
        return render(request, 'login.html', context)
    else:
        print('Error on request (not GET/POST)')


def dashboard(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user, _ = UserProfile.objects.get_or_create(user=request.user)
            form = UpdateUserProfileForm()
            form.fields['username'].initial = user.user.username
            form.fields['defaultCounty'].initial = user.defaultCounty
            return render(request, 'dashboard.html', {'form': form, 'user': user})
        elif request.method == 'POST':
            form = UpdateUserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                userProfile = UserProfile.objects.get(user=request.user)
                user = userProfile.user
                context = {}
                success_fields = []
                error_fields = []
                if form.cleaned_data['avatar']:
                    userProfile.avatar = form.cleaned_data['avatar']
                    success_fields.append('相片')
                if form.cleaned_data['username'] != '' and form.cleaned_data['username'] != user.username:
                    user.username = form.cleaned_data['username']
                    success_fields.append('名稱')
                if form.cleaned_data['defaultCounty'] != '' and form.cleaned_data['defaultCounty'] != userProfile.defaultCounty:
                    userProfile.defaultCounty = form.cleaned_data['defaultCounty']
                    success_fields.append('預設顯示城市')
                if form.cleaned_data['password'] != '' or form.cleaned_data['password_confirm'] != '':
                    if form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
                        user.set_password(form.cleaned_data['password'])
                        success_fields.append('密碼')
                    else:
                        error_fields.append('密碼不一致')
                if success_fields.__len__() > 0:
                    user.save()
                    userProfile.save()
                    context['success_message'] = f'更新成功({", ".join(success_fields)})'
                if error_fields.__len__() > 0:
                    context['err_message'] = f'更新失敗({", ".join(error_fields)})'
                renderForm = UpdateUserProfileForm()
                renderForm.fields['username'].initial = user.username
                renderForm.fields['defaultCounty'].initial = userProfile.defaultCounty
                context['form'] = renderForm
                context['user'] = userProfile
                return render(request, 'dashboard.html', context)
            else:
                return render(request, 'dashboard.html', {'form': form, 'user': user, 'err_message': '表單驗證錯誤'})
    else:
        return redirect('/user/login')


def signup(request):
    if request.method == 'GET':
        signup_form = SignupForm()
        context = {
            'user': request.user,
            'signup_form': signup_form,
        }
        return render(request, 'signup.html', context)
    elif request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data['username']
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            user = User.objects.create_user(
                username=username, email=email, password=password)
            # username
            # password
            # email
            # first_name
            # last_name
            user.save()
            userProfile = UserProfile(user=user)
            userProfile.save()
            context = {
                'success_signup_msg': '註冊成功，請點選登入',
            }
            return render(request, 'signup.html', context)
        else:
            err_signup_msg = '註冊失敗，請填入有效的帳號密碼'

        # signup fail
        context = {
            'signup_form': signup_form,
            'err_signup_msg': err_signup_msg
        }
        return render(request, 'signup.html', context)
    else:
        print('Error on request (not GET/POST)')


def logout(request):
    auth.logout(request)
    return redirect('/')
