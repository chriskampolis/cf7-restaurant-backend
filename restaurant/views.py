from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, MenuItem, Order, OrderItem
from .serializers import UserSerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer, OrderItemUpdateSerializer
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
    serializer_class = OrderSerializer
    queryset = Order.objects.prefetch_related('items', 'items__menu_item')
    permission_classes = [permissions.IsAuthenticated] # Both employees and / or managers can place orders

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.prefetch_related('items', 'items__menu_item')

        if not user.is_manager():
            queryset = queryset.filter(placed_by=user)
        table = self.request.query_params.get('table')
        if table: 
            queryset = queryset.filter(table_number=table)
        return queryset
    
    @action(detail=True, methods=['post'], url_path='add-items')
    def add_items(self, request, pk=None):
        order = self.get_object()
        serializer = OrderItemSerializer(data=request.data, many=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        for item_data in serializer.validated_data:
            try:
                OrderItem.objects.create(order=order, **item_data)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Items added successfully."}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'], url_path='update_item')
    def update_item(self, request, pk=None):
        order = self.get_object()
        serializer = OrderItemUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        try:
            # Replace an item: remove old / add new
            if data.get('old_menu_item') and data.get('new_menu_item'):
                old_item = order.items.get(menu_item__id=data['old_menu_item'])
                old_item.restore_stock_and_delete()

                new_menu_item = MenuItem.objects.get(id=data['new_menu_item'])
                OrderItem.objects.create(order=order, menu_item=new_menu_item, quantity=data['quantity'])
                return Response({"message": "Item replaced successfully."}, status=status.HTTP_200_OK)
            
            # Delete item
            elif data.get('menu_item') and data.get('quantity') == 0:
                item = order.items.get(menu_item__id=data['menu_item'])
                item.restore_stock_and_delete()
                return Response({"message": "Item removed successfully."}, status=status.HTTP_200_OK)
            
            # Update quantity
            elif data.get('menu_item') and 'quantity' in data:
                item = order.items.get(menu_item__id=data['menu_item'])
                item.update_quantity(data['quantity'])
                return Response({"message": "Item updated successfully."}, status=status.HTTP_200_OK)
            
        except (OrderItem.DoesNotExist, MenuItem.DoesNotExist):
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
