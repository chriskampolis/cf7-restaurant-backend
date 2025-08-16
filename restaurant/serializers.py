from rest_framework import serializers
from .models import User, MenuItem, OrderItem, Order

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'username', 'password', 'role']
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
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        # Check if an active order exists for this table
        if Order.objects.filter(table_number=validated_data['table_number'], status='in_progress').exists():
            raise serializers.ValidationError("An active order already exists for this table.")

        order = Order.objects.create(placed_by=user, **validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
    
# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['menu_item', 'quantity']

# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)
#     total_price = serializers.ReadOnlyField()

#     class Meta:
#         model = Order
#         fields = ['id', 'table_number', 'placed_by', 'created_at', 'items', 'total_price'] 
#         read_only_fields = ['placed_by', 'created_at', 'total_price']
    
#     def create(self, validated_data):
#         items_data = validated_data.pop('items')
#         user = self.context['request'].user
#         order = Order.objects.create(placed_by=user, **validated_data)

#         # Delete all items from this order - use restore stock and delete and save new (updated order)
#         """ Create each OrderItem and trigger availability logic in OrderItem.save() """
#         for item_data in items_data:
#             item = OrderItem(order=order, **item_data)
#             item.save() 
        
#         return order

# class OrderItemUpdateSerializer(serializers.Serializer):
#     old_menu_item = serializers.IntegerField(required=False)
#     new_menu_item = serializers.IntegerField(required=False)
#     old_quantity = serializers.IntegerField(required=False, min_value=1)
#     new_quantity = serializers.IntegerField(required=False, min_value=1)
#     menu_item = serializers.IntegerField(required=False)
#     quantity = serializers.IntegerField(required=False, min_value=0)

#     def validate(self, data):
#         old_item = data.get("old_menu_item")
#         new_item = data.get("new_menu_item")
#         menu_item = data.get("menu_item")
#         quantity = data.get("quantity")
#         old_qty = data.get("old_quantity")
#         new_qty = data.get("new_quantity")

#         # Replacement logic
#         if old_item and new_item:
#             if old_qty is None:
#                 raise serializers.ValidationError("old_quantity is required when replacing items.")
#             if new_qty is None:
#                 raise serializers.ValidationError("new_quantity is required when replacing items.")
#             return data
        
#         # Update / Delete logic
#         if menu_item is not None:
#             if quantity is None:
#                 raise serializers.ValidationError("Quantity is required when specifying menu_item.")
#             return data
        
#         raise serializers.ValidationError(
#             "Provide either (old_menu_item, new_menu_item, old_quantity, new_quantity) for replacement, "
#             "or (menu_item, quantity) for update/delete."
#             )