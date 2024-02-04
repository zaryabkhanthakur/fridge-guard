from django.urls import path
from .views import HomeView, login, logout

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('', login, name="login" ),
    path('home/', HomeView.as_view(), name='home')
]
