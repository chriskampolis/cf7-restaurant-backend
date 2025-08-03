# from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MenuItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = router.urls