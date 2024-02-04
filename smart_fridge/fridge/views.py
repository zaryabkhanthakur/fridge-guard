from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as authlogin, authenticate, logout as authlogout
from django.urls import reverse_lazy

from .models import Suplier


def login(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        auth_form = AuthenticationForm(request, data=request.POST)
        if auth_form.is_valid():
            name = auth_form.cleaned_data.get("username")
            password = auth_form.cleaned_data.get("password")
            user = authenticate(username=name, password=password)
            if user is not None:
                authlogin(request, user)
                messages.info(request, f"Welcome, {name}!")
                print("hello")
                return redirect("home")
            else:
                print("invalid user name")
                messages.error(request, "Invalid username or password")
        else:
            print(auth_form.errors)
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request=request, template_name="fridge/login.html", context={"login_form": form})


def logout(request):
    authlogout(request)
    messages.info(request, "You have successfully logged out")
    return redirect('login')


class SupplierView(LoginRequiredMixin, ListView):
    model = Suplier
    context_object_name = "supplier_list"
    template_name = "fridge/supplier.html"


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("fridge:login")
    template_name = "fridge/home.html"
