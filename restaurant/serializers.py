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
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'placed_by', 'created_at', 'items']
        read_only_fields = ['placed_by', 'created_at']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(placed_by=user, **validated_data)

        """ Create each OrderItem and trigger availability logic in OrderItem.save() """
        for item_data in items_data:
            item = OrderItem(order=order, **item_data)
            item.save() 
        
        return order

class OrderItemUpdateSerializer(serializers.Serializer):
    old_menu_item = serializers.IntegerField(required=False)
    new_menu_item = serializers.IntegerField(required=False)
    old_quantity = serializers.IntegerField(required=False, min_value=1)
    new_quantity = serializers.IntegerField(required=False, min_value=1)
    menu_item = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False, min_value=0)

    def validate(self, data):
        old_item = data.get("old_menu_item")
        new_item = data.get("new_menu_item")
        menu_item = data.get("menu_item")
        quantity = data.get("quantity")
        old_qty = data.get("old_quantity")
        new_qty = data.get("new_quantity")

        # Replacement logic
        if old_item and new_item:
            if old_qty is None:
                raise serializers.ValidationError("old_quantity is required when replacing items.")
            if new_qty is None:
                raise serializers.ValidationError("new_quantity is required when replacing items.")
            return data
        
        # Update / Delete logic
        if menu_item is not None:
            if quantity is None:
                raise serializers.ValidationError("Quantity is required when specifying menu_item.")
            return data
        
        raise serializers.ValidationError(
            "Provide either (old_menu_item, new_menu_item, old_quantity, new_quantity) for replacement, "
            "or (menu_item, quantity) for update/delete."
            )