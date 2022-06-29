from asyncore import read
from dataclasses import field
from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = '__all__'
class ProductRasmiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rasmi
      

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rasm
        fields = ['id', 'file_field', 'title', 'rasmlar']


class CategorySerializer(serializers.ModelSerializer):
    # category = MassageSerializer(many=True, read_only=True)
    rasmlar= FileSerializer(many= True, read_only=True)
    class Meta:
        model = Categoriya
        fields = ['id','categoriya_nomi', 'rasmlar' ]