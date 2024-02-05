from django.urls import path
from .views import HomeView, SupplierView, FridgeItemView, FridgeItemCreateView, ChefListView, RiderViewList
from .views import login, logout, create_user

app_name = "fridge"
urlpatterns = [
    path('logout/', logout, name='logout'),
    path('', login, name="login" ),
    path('create_user/', create_user, name="create_user"),
    path('chefs/', ChefListView.as_view(), name='chefs'),
    path('riders/', RiderViewList.as_view(), name='riders'),
    path('home/', HomeView.as_view(), name='home'),
    path('items/', FridgeItemView.as_view(), name='items'),
    path('items/add', FridgeItemCreateView.as_view(), name="add_item"),
    path('suppliers/', SupplierView.as_view(), name="suppliers")
]
