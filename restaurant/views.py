from rest_framework import viewsets, permissions
from .models import User, MenuItem, Order
from .serializers import UserSerializer, MenuItemSerializer, OrderSerializer
from .permissions import IsManager, IsManagerOrReadOnlyMenuItem

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]  # Only managers can CRUD users

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnlyMenuItem]  # Employees read-only, managers CRUD

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated] # Both employees and / or managers can place orders

    def get_queryset(self):
        # Users see their orders only, unless they are manager
        user = self.request.user
        if user.is_manager():
            return Order.objects.all()
        return Order.objects.filter(placed_by=user)