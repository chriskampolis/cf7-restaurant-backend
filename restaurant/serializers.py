from rest_framework import serializers
from .models import User, MenuItem, OrderItem, Order

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "price", "availability", "category"]

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'password', 'role']
        extra_kwargs = {"password": {"write_only":True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    price = serializers.DecimalField(source='menu_item.price', max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    placed_by = serializers.StringRelatedField(read_only=True)
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'placed_by', 'status', 'created_at', 'total_price', 'items']
        read_only_fields = ['placed_by', 'status', 'created_at', 'total_price']

    def create(self, validated_data):
        """
        Create an order with its items.
        Prevents multiple active orders for the same table.
        """
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        # Check if an active order exists for this table
        if Order.objects.filter(table_number=validated_data['table_number'], status='in_progress').exists():
            raise serializers.ValidationError("An active order already exists for this table.")

        order = Order.objects.create(placed_by=user, **validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

# Used for listing completed orders (read-only, auditing purposes)
class CompletedOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Order
        fields = ["id", "table_number", "created_at", "items", "total_price"]