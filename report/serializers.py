from dataclasses import field
from .models import *

from rest_framework import serializers

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductList
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'