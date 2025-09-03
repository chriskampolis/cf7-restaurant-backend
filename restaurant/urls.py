from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CompletedOrdersView, UserViewSet, MenuItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = router.urls + [
    path("completed-orders/", CompletedOrdersView.as_view(), name="completed-orders"),
]