from django.shortcuts import render, redirect
from .forms import CreateUserForm

def homepage(request):
    return render(request, 'index.html')

def my_login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    context = {'registerform': form}
    return render(request, 'register.html', context=context)
