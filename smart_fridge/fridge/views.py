from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as authlogin, authenticate, logout as authlogout
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.decorators import login_required


from .models import Suplier, FridgeItem, Notification, Order
from .forms import UserCreationForm, RiderInsertionForm, ChefInsertionFrom, ChefRemoveFrom


content_type = ContentType.objects.get_for_model(FridgeItem)
fridge_permissions = Permission.objects.filter(content_type=content_type)
print([perm.codename for perm in fridge_permissions])


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
        create_form = UserCreationForm(data=request.POST)
        if create_form.is_valid():
            username = create_form.cleaned_data.get("username")
            email = create_form.cleaned_data.get("email")
            role = create_form.cleaned_data.get("role")
            password = create_form.cleaned_data.get("password")
            print(role)
            user = User.objects.create_user(
                username=username, email=email, password=password)

            can_insert_item = Permission.objects.get(codename='add_fridgeitem')
            can_open_fridge = Permission.objects.get(
                codename='view_fridgeitem')

            if role == 'Chef':
                can_remove_item = Permission.objects.get(
                    codename='change_fridgeitem')
                user.user_permissions.add(can_remove_item)

            user.user_permissions.add(can_insert_item, can_open_fridge)

            group = Group.objects.get(name=role)
            user.groups.add(group)

            user.save()

            messages.success(request, "User has been added successfully")
        else:
            messages.error(request, "Something went wrong")
    create_form = UserCreationForm()

    return render(request, "fridge/create_form.html", {'form': create_form})


@login_required
def insert_item(request):
    if request.user.groups.filter(name="Chef"):
        print("here")
        if request.method == 'POST':
            form = ChefInsertionFrom(request.POST)
            if form.is_valid():
                item = form.cleaned_data.get('item')
                quanity = form.cleaned_data.get('quantity')
                item.insert_item(quanity, request.user)
                return redirect("fridge:home")
        else:
            form = ChefInsertionFrom()

        return render(request, "fridge/add_item.html", {'form': form})
    if request.user.groups.filter(name="Rider"):
        print("rider")
        if request.method == 'POST':
            form = RiderInsertionForm(request.POST)

            if form.is_valid():
                order_code = form.cleaned_data.get("order_code")
                order = Order.objects.get(order_code=order_code)
                order.update_order_statue()
                return redirect("fridge:order_detail", pk=order.pk)
            print("not valid")
            print(form.errors)
        else:
            form = RiderInsertionForm()

        return render(request, "fridge/add_item.html", {'form': form})
    print("returning here")
    return redirect("fridge:home")


@login_required
def remove_item(request):
    if request.user.groups.filter(name="Chef"):
        print("here")
        if request.method == 'POST':
            form = ChefRemoveFrom(request.POST)
            if form.is_valid():
                item = form.cleaned_data.get('item')
                quanity = form.cleaned_data.get('quantity')
                item.take_item(quanity, request.user)
                return redirect("fridge:home")
        else:
            form = ChefRemoveFrom()
        return render(request, "fridge/add_item.html", {'form': form})
    return redirect("fridge:home")


class FridgeItemExpiredView(LoginRequiredMixin, ListView):
    model = FridgeItem
    context_object_name = "items"
    template_name = "fridge/fridge_item.html"

    def get_queryset(self):
        now = timezone.now()
        queryset = FridgeItem.objects.filter(expiry_date__lt=now)
        return queryset
    
class FridgeItemFreshView(LoginRequiredMixin, ListView):
    model = FridgeItem
    context_object_name = "items"
    template_name = "fridge/fridge_item.html"

    def get_queryset(self):
        now = timezone.now()
        queryset = FridgeItem.objects.filter(expiry_date__gt=now)
        return queryset


class FridgeItemView(LoginRequiredMixin, ListView):
    model = FridgeItem
    context_object_name = "items"
    template_name = "fridge/fridge_item.html"


class FridgeItemCreateView(LoginRequiredMixin, CreateView):
    model = FridgeItem
    fields = ["name", "quantity", "min_reminder", "expiry_date",
              "auto_order", "supplier", "default_order_quantity"]
    template_name = "fridge/create_form.html"

    def get_success_url(self):
        return reverse_lazy('fridge:items')


permission_mapping = {
    'add_fridgeitem': 'Insert',
    'change_fridgeitem': 'Remove',
    'view_fridgeitem': 'Open',
}


class ChefListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "users"

    template_name = "fridge/user_list.html"

    def get_queryset(self):
        queryset = User.objects.prefetch_related(
            'user_permissions').filter(groups__name="Chef")
        print(queryset[0].get_all_permissions())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["permission_mapping"] = permission_mapping

        return context


class RiderViewList(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "users"

    template_name = "fridge/user_list.html"

    def get_queryset(self):
        queryset = User.objects.filter(groups__name="Rider")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["permission_mapping"] = permission_mapping

        return context


class SupplierView(LoginRequiredMixin, ListView):
    model = Suplier
    context_object_name = "suppliers_list"
    template_name = "fridge/supplier_list.html"


class SupplierCreaetView(LoginRequiredMixin, CreateView):
    model = Suplier
    fields = ["name", "address", "email", "phone"]
    template_name = "fridge/create_form.html"

    def get_success_url(self):
        return reverse_lazy('fridge:suppliers')


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("fridge:login")
    template_name = "fridge/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notifications"] = Notification.objects.filter(
            is_read=False).count()

        return context


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "fridge/updates.html"
    context_object_name = "notifications"

    def get_queryset(self):
        queryset = Notification.objects.all().order_by("-created_at")
        return queryset


class ExpiryNotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "fridge/updates.html"
    context_object_name = "notifications"

    def get_queryset(self):
        queryset = Notification.objects.filter(
            type='item_expired').order_by("-created_at")
        queryset.update(is_read=True)
        return queryset


class OrdersNotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "fridge/updates.html"
    context_object_name = "notifications"

    def get_queryset(self):
        queryset = Notification.objects.filter(
            type__contains='order').order_by("-created_at")
        queryset.update(is_read=True)
        return queryset


class StockNotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "fridge/updates.html"
    context_object_name = "notifications"

    def get_queryset(self):
        queryset = Notification.objects.filter(
            type__in=['item_removed', 'item_ inserted']).order_by("-created_at")
        queryset.update(is_read=True)
        return queryset


class FridgeOpenNotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "fridge/updates.html"
    context_object_name = "notifications"

    def get_queryset(self):
        queryset = Notification.objects.filter(
            type="fridge_opened").order_by("-created_at")
        queryset.update(is_read=True)
        queryset_copy = queryset
        return queryset_copy


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "fridge/object_detail.html"


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "fridge/order_list.html"
    context_object_name = "orders"
    
    def get_queryset(self):
        return Order.objects.all().order_by('-created_at')
class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ["firdge_item", "supplier", "quantity", "expiry_date"]
    template_name = "fridge/create_form.html"

    def get_success_url(self):
        return reverse_lazy('fridge:order_list')