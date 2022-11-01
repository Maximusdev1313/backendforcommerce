from re import L
from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet

class ReportViewSet(ModelViewSet):
    queryset = ProductList.objects.all()
    serializer_class = ProductListSerializer

class ScoreViewSet(ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer