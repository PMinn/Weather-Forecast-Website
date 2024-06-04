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
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                err_login_msg = 'Login failed (user id/passworld not correct)'
        else:
            err_login_msg = 'Login error (login form is not valid)'

        # login fail
        context = {
            'login_form': login_form,
            'err_login_msg': err_login_msg
        }
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
                needSave = False
                if form.cleaned_data['avatar']:
                    userProfile.avatar = form.cleaned_data['avatar']
                    needSave = True
                if form.cleaned_data['username'] != '' and form.cleaned_data['username'] != user.username:
                    user.username = form.cleaned_data['username']
                    needSave = True
                if form.cleaned_data['defaultCounty'] != '' and form.cleaned_data['defaultCounty'] != userProfile.defaultCounty:
                    userProfile.defaultCounty = form.cleaned_data['defaultCounty']
                    needSave = True
                if form.cleaned_data['password'] != '' and form.cleaned_data['password_confirm'] != '' and form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
                    user.set_password(form.cleaned_data['password'])
                    needSave = True
                if needSave:
                    user.save()
                    userProfile.save()
                form = UpdateUserProfileForm()
                form.fields['username'].initial = user.username
                form.fields['defaultCounty'].initial = userProfile.defaultCounty
                return render(request, 'dashboard.html', {'form': form, 'user': userProfile, 'success_message': '更新成功'})
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
            context = {
                'success_signup_msg': '註冊成功，請點選登入',
            }
            return render(request, 'signup.html', context)
        else:
            err_signup_msg = 'signup error (signup form is not valid)'

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
