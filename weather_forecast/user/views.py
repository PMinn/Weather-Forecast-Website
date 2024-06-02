from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib import auth
from .forms import LoginForm, SignupForm
from django.contrib.auth.models import User

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
                # context = {
                #     'user': request.user,
                #     'message': 'login ok'
                # }
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
