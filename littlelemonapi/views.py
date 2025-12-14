from django.contrib.auth.models import User, Group
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from .models import MenuItem, Cart, Order
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer
from .permissions import IsManager,IsDeliveryCrew

class GroupUserManagementView(APIView):
    """
    Generic API view to manage users in groups.
    """
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def get_group(self):
        group_name = self.kwargs['group_name']
        return Group.objects.get(name=group_name)

    def get(self, request, *args, **kwargs):
        group = self.get_group()
        users = group.user_set.all()
        return Response(
            [{"id": user.id, "username": user.username, "email": user.email} for user in users]
        )

    def post(self, request, *args, **kwargs):
        group = self.get_group()
        username = request.data.get("username")

        try:
            user = User.objects.get(username=username)
            group.user_set.add(user)
            return Response({"message": f"User '{username}' added to {group.name} group."}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        group = self.get_group()
        username = request.data.get("username")

        try:
            user = User.objects.get(username=username)
            group.user_set.remove(user)
            return Response({"message": f"User '{username}' removed from {group.name} group."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [permissions.IsAuthenticated(), IsManager()]
        return [permissions.AllowAny()]


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsManager()]
        return [permissions.AllowAny()]

class CartListCreateView(generics.ListCreateAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDeleteView(generics.DestroyAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return Order.objects.all()
        elif user.groups.filter(name="Delivery Crew").exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


