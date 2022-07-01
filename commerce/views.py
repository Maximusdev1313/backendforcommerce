from django.shortcuts import render

# Create your views here.
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRasmiViewSet(ModelViewSet):
    queryset = ProductRasmi.objects.all()
    serializer_class = ProductRasmiSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Categoriya.objects.all()
    serializer_class = CategorySerializer

class RasmViewSet(ModelViewSet):
    queryset = Rasm.objects.all()
    serializer_class = FileSerializer