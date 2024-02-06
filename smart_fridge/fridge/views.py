from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as authlogin, authenticate, logout as authlogout
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy, reverse
from django.conf import settings

from .models import Suplier, FridgeItem, Notification
from .forms import UserCreationForm


def login(request):
    if request.user.is_authenticated:
        return redirect("fridge:home")

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
                return redirect("fridge:home")
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
    return redirect('fridge:login')



def create_user(request):
    if request.user.is_superuser and request.method == 'POST':
        create_form = UserCreationForm( data=request.POST)
        if create_form.is_valid():
            username = create_form.cleaned_data.get("username")
            email = create_form.cleaned_data.get("email")
            role = create_form.cleaned_data.get("role")
            password = create_form.cleaned_data.get("password")
            print(role)
            user = User.objects.create_user(username=username, email=email, password=password)
            group = Group.objects.get(name=role)
            user.groups.add(group)
            messages.success(request, "User has been added successfully")
        else:
            messages.error(request, "Something went wrong")
    create_form = UserCreationForm()    
        
    return render(request, "fridge/create_form.html", {'form': create_form})
     
            
class FridgeItemView(LoginRequiredMixin, ListView):
     model = FridgeItem
     context_object_name = "items"
     template_name = "fridge/fridge_item.html"     

class FridgeItemCreateView(LoginRequiredMixin, CreateView):
    model = FridgeItem
    fields = ["name", "quantity", "min_reminder", "expiry_date", "auto_order"]
    template_name = "fridge/create_form.html"
    def get_success_url(self):
        return reverse_lazy('fridge:items')
    
class ChefListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "users"

    template_name = "fridge/user_list.html"
    
    def get_queryset(self):
        queryset = User.objects.filter(groups__name="Chef")
        print(queryset[0].get_all_permissions())
        return queryset
    
class RiderViewList(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "users"

    template_name = "fridge/user_list.html"
    
    def get_queryset(self):
        queryset = User.objects.filter(groups__name="Rider")
        return queryset


class SupplierView(LoginRequiredMixin, ListView):
    model = Suplier
    context_object_name = "suppliers_list"
    template_name = "fridge/supplier_list.html"


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("fridge:login")
    template_name = "fridge/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notifications"] = Notification.objects.filter(is_read=False).count()

        return context