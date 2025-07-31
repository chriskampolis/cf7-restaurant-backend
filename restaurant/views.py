from rest_framework import viewsets
from .models import User, MenuItem
from .serializers import UserSerializer, MenuItemSerializer
from .permissions import IsManager, IsManagerOrReadOnlyMenuItem

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]  # Only managers can CRUD users

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnlyMenuItem]  # Employees read-only, managers CRUD

# from django.shortcuts import render
# from django.contrib.auth.models import User
# from rest_framework import generics
# from .models import User
# from .serializers import UserSerializer
# from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

# class IsManager(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == 'manager'


# class CreateUserView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]