from django.urls import path
from .views import (HomeView, SupplierView, FridgeItemView, FridgeItemCreateView,
                    ChefListView, RiderViewList, SupplierCreaetView, NotificationListView,
                    StockNotificationListView, ExpiryNotificationListView, OrdersNotificationListView,
                    FridgeOpenNotificationListView, OrderDetailView, FridgeItemExpiredView,
                    FridgeItemFreshView, OrderListView, OrderCreateView)
from .views import login, logout, create_user, insert_item, remove_item

app_name = "fridge"
urlpatterns = [
    path('logout/', logout, name='logout'),
    path('', login, name="login"),
    path('create_user/', create_user, name="create_user"),
    path('chefs/', ChefListView.as_view(), name='chefs'),
    path('riders/', RiderViewList.as_view(), name='riders'),
    path('home/', HomeView.as_view(), name='home'),
    path('updates/', NotificationListView.as_view(), name="updates"),
    path('updates/stocks', StockNotificationListView.as_view(), name="stock_updates"),
    path('updates/expiry', ExpiryNotificationListView.as_view(),
         name="expiry_updates"),
    path('updates/order', OrdersNotificationListView.as_view(), name="order_updates"),
    path('updates/access', FridgeOpenNotificationListView.as_view(),
         name="fridge_updates"),
    path('items/all', FridgeItemView.as_view(), name='items'),
    path('items/expired', FridgeItemExpiredView.as_view(), name='items_expired'),
    path('items/fresh', FridgeItemFreshView.as_view(), name='items_fresh'),
    path('items/add', FridgeItemCreateView.as_view(), name="add_item"),
    path('orders/all', OrderListView.as_view(), name="order_list"),
    path('orders/create/', OrderCreateView.as_view(), name='order_detail'),

    path('items/insert',  insert_item, name="insert_item"),
    path('items/take', remove_item, name='remove-item'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('suppliers/', SupplierView.as_view(), name="suppliers"),
    path('suppliers/add', SupplierCreaetView.as_view(), name='add_supplier')
]
