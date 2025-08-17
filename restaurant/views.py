from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, MenuItem, Order, OrderItem
from .serializers import UserSerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer
from .permissions import IsManager, IsManagerOrReadOnlyMenuItem

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
    permission_classes = [IsManagerOrReadOnlyMenuItem]  # Employees read-only, managers CRUD

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().select_related('placed_by').prefetch_related('items__menu_item')
    permission_classes = [IsAuthenticated] # Both employees and / or managers can place orders

    def get_queryset(self): # do not restrict employees to their orders only - keep as it is.
        table = self.request.query_params.get('table')
        queryset = super().get_queryset()
        if table:
            queryset = queryset.filter(table_number=table)
        return queryset

    @action(detail=False, methods=['post'], url_path='submit')
    def submit_order(self, request):
        """
        Creates a new in_progress order if none exists for the table.
        If one exists, replaces all items.
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
    
    # @action(detail=True, methods=['post'], url_path='add-items')
    # def add_items(self, request, pk=None):
    #     order = self.get_object()
    #     serializer = OrderItemSerializer(data=request.data, many=True)

    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #     for item_data in serializer.validated_data:
    #         menu_item = item_data['menu_item']
    #         quantity = item_data['quantity']

    #         try:
    #             # Try to increase the quantity of an existing item in the order - instead of creating duplicate
    #             existing_item = OrderItem.objects.get(order=order, menu_item=menu_item)
    #             try:
    #                 existing_item.update_quantity(existing_item.quantity + quantity)
    #             except ValueError as e:
    #                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #         except OrderItem.DoesNotExist:
    #             # Add new item for the specified order
    #             try:
    #                 OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity)
    #             except ValueError as e:
    #                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({"message": "Items added successfully."}, status=status.HTTP_201_CREATED)
    
    # @action(detail=True, methods=['patch'], url_path='update-item')
    # def update_item(self, request, pk=None):
    #     order = self.get_object()
    #     serializer = OrderItemUpdateSerializer(data=request.data)

    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #     data = serializer.validated_data
        
    #     try:
    #         # Partial replacement
    #         if data.get('old_menu_item') and data.get('new_menu_item'):
    #             old_item = order.items.get(menu_item__id=data['old_menu_item'])

    #             if old_item.quantity < data['old_quantity']:
    #                 return Response({"error": "Not enough quantity to replace"}, status=status.HTTP_400_BAD_REQUEST)
                
    #             # Reduce or delete old item
    #             if old_item.quantity == data['old_quantity']:
    #                 old_item.restore_stock_and_delete()
    #             else:
    #                 old_item.update_quantity(old_item.quantity - data['old_quantity'])
                
    #             # Add or update new item
    #             new_menu_item = MenuItem.objects.get(id=data['new_menu_item'])
    #             try:
    #                 new_item = order.items.get(menu_item=new_menu_item)
    #                 new_item.update_quantity(new_item.quantity + data['new_quantity'])
    #             except:
    #                 OrderItem.objects.create(order=order, menu_item=new_menu_item, quantity=data['new_quantity'])
                    
    #             return Response({"message": "Item replaced successfully."}, status=status.HTTP_200_OK)
            
    #         # Delete item
    #         elif data.get('menu_item') and data.get('quantity') == 0:
    #             item = order.items.get(menu_item__id=data['menu_item'])
    #             item.restore_stock_and_delete()
    #             return Response({"message": "Item removed successfully."}, status=status.HTTP_200_OK)
            
    #         # Update quantity
    #         elif data.get('menu_item') and 'quantity' in data:
    #             item = order.items.get(menu_item__id=data['menu_item'])
    #             item.update_quantity(data['quantity'])
    #             return Response({"message": "Item updated successfully."}, status=status.HTTP_200_OK)
            
    #     except (OrderItem.DoesNotExist, MenuItem.DoesNotExist):
    #         return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
    #     except ValueError as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
