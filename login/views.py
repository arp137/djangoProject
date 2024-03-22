from django.shortcuts import render, redirect
from . forms import CreateUserForm

from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def homepage(request):
    return render(request, 'login/index.html')


def my_login(request):
    return render(request, 'login/login.html')


def dashboard(request):
    return render(request, 'login/dashboard.html')

def register(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my-login")

    context = {'registerform':form}

    return render(request, 'login/register.html', context=context)