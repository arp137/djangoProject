from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login



def homepage(request):
    return render(request, 'homepage.html')


# Vista de inicio de sesión personalizada
def my_login(request):
    form = LoginForm(request.POST or None)
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:  # Procede solo si ambos campos no están vacíos
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("dashboard")
            else:
                error_message = "Your username or password is incorrect. Please try again."
        else:
            error_message = "Both username and password are required."

    context = {'loginform': form, 'error_message': error_message}
    return render(request, 'login.html', context=context)


@login_required(login_url="login")
def dashboard(request):
    return render(request, 'dashboard.html')


def register(request):
    error_message = ''

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            error_message = form.errors.as_text()
            error_message = error_message.replace('password2', 'password')
    else:
        form = CreateUserForm()

    context = {'registerform': form, 'error_message': error_message}
    return render(request, 'register.html', context=context)


def user_logout(request):
    auth.logout(request)
    return redirect('')
