from django.urls import path
from .views import (
    MenuItemListCreateView, MenuItemDetailView,
    CartListCreateView, CartDeleteView,
    OrderListCreateView, GroupUserManagementView
)

urlpatterns = [
    path('menu-items/', MenuItemListCreateView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>/', MenuItemDetailView.as_view(), name='menu-item-detail'),

    path('cart/', CartListCreateView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartDeleteView.as_view(), name='cart-delete'),

    path('orders/', OrderListCreateView.as_view(), name='orders'),
    # Role management endpoints
    path('groups/<str:group_name>/users/', GroupUserManagementView.as_view(), name="group-users"),
]
