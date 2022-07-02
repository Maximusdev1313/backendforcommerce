from dataclasses import field
from .models import *

from rest_framework import serializers

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'