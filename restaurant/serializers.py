from rest_framework import serializers
from .models import User, MenuItem

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
    
# class ReservationSerializer(serializers.ModelSerializer):
#     class Meta: 
#         model = Reservation
#         fields = '__all__'
