from django import forms
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login as auth_login
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import CreateView


class HomePageView(generic.TemplateView):
    template_name = 'homepage.html'


# Vista de inicio de sesión personalizada

class LoginFormLogin(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class MyLoginView(generic.TemplateView):
    template_name = 'login.html'
    form_class = LoginFormLogin
    success_url = '/dashboard/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(self.success_url)
            else:
                form.add_error(None, "Your username or password is incorrect. Please try again.")

        return render(request, self.template_name, {'form': form})


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = '/login/'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        error_message = form.errors.as_text().replace('password2', 'password')
        return self.render_to_response(self.get_context_data(form=form, error_message=error_message))


def user_logout(request):
    auth.logout(request)
    return redirect('')
