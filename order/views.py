from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet

# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
