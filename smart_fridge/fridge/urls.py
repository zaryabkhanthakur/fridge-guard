from django.urls import path
from .views import HomeView, login, logout, SupplierView, create_user

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('', login, name="login" ),
    path('create_user/', create_user, name="create_user"),
    path('home/', HomeView.as_view(), name='home'),
    path('suppliers/', SupplierView.as_view(), name="suppliers")
]
