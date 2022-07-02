from re import L
from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet

class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer