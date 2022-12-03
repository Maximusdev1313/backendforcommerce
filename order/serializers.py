from .models import *

from rest_framework import serializers


    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product_name', 'weight', 'litr' , 'quantity', 'price', 'total_price', 'orderForUser']

class UserSerializer(serializers.ModelSerializer):
    orderForUser = OrderSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id','ip_address', 'userName', 'phoneNumber', 'address', 'location', 'tages',  'comment', 'time', 'orderForUser', 'ready', 'total']