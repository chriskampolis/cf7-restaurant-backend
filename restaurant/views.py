from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, MenuItem, Order, OrderItem
from .serializers import UserSerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer, CompletedOrderSerializer
from .permissions import IsManager, ReadOnlyOrIsManager

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]  # Only managers can CRUD users

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Returns the currently authenticated user.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [ReadOnlyOrIsManager] # Employees can read, only managers can edit

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().select_related('placed_by').prefetch_related('items__menu_item')
    permission_classes = [IsAuthenticated] # Any logged-in employee/manager can create orders

    def get_queryset(self):
        """Optionally filter orders by table number (e.g. ?table=3)."""
        table = self.request.query_params.get('table')
        queryset = super().get_queryset()
        if table:
            queryset = queryset.filter(table_number=table)
        return queryset

    @action(detail=False, methods=['post'], url_path='submit')
    def submit_order(self, request):
        """
        Submit a new order or update an existing in-progress order for a table.
        If updating, old items are removed and replaced with new ones.
        """
        table_number = request.data.get('table_number')
        items_data = request.data.get('items', [])

        if not table_number or not isinstance(items_data, list) or not items_data:
            return Response({"error": "table_number and items are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for existing in-progress order
        order = Order.objects.filter(table_number=table_number, status='in_progress').first()

        if not order:
            # Create a new order
            order = Order.objects.create(
                table_number=table_number,
                placed_by=request.user,
                status='in_progress'
            )
        else:
            # Replace all items (only if in progress)
            if order.status != 'in_progress':
                return Response({"error": "Cannot update a completed order."}, status=status.HTTP_400_BAD_REQUEST)
            for item in order.items.all():
                item.restore_stock_and_delete()

        # Add new items
        for item_data in items_data:
            serializer = OrderItemSerializer(data=item_data)
            serializer.is_valid(raise_exception=True)
            OrderItem.objects.create(order=order, **serializer.validated_data)

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='complete')
    def complete_order(self, request, pk=None):
        """
        Marks an order as completed — cannot be updated after this.
        """
        try:
            order = self.get_object()
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.status == 'completed':
            return Response({"error": "Order is already completed."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'completed'
        order.save(update_fields=['status'])

        return Response({"message": f"Order {order.id} marked as completed."}, status=status.HTTP_200_OK)

class CompletedOrdersView(generics.ListAPIView):
    serializer_class = CompletedOrderSerializer
    permission_classes = [IsManager]   # managers only

    def get_queryset(self):
        """Return all completed orders sorted by most recent first."""
        return Order.objects.filter(status="completed").order_by("-created_at")