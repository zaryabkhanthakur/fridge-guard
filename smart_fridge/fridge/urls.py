from django.urls import path
from .views import HomeView, login, logout, SupplierView

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('', login, name="login" ),
    path('home/', HomeView.as_view(), name='home'),
    path('suppliers/', SupplierView.as_view(), name="suppliers")
]
