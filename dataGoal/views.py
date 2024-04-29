from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import api
from django.http import JsonResponse


@login_required(login_url="login")
def dashboard(request):
    algo = api.get_example()
    context = algo
    return render(request, 'dashboard.html', {'data': context})

