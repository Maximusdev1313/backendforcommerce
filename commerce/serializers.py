
from asyncore import read
from rest_framework import serializers
from .models import *

class ProductRasmiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRasmi
        fields = ['id', 'title', 'link', 'rasmlari']
class ProductSerializer(serializers.ModelSerializer):
    rasmlari = ProductRasmiSerializer(many= True, read_only=True)
    class Meta: 
        model = Product
        fields = ['id', 'nomi', 'kilogramm', 'litri', 'soni', 'narx', 'eski_narx', 'chegirma_foizi', 'kerakli' ,'time',  'mahsulot', 'rasmlari']
    def __str__(self):
        return self.nomi


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriyaRasm
        fields = ['id', 'link', 'title', 'rasmlar']


class CategorySerializer(serializers.ModelSerializer):
    # category = MassageSerializer(many=True, read_only=True)
    rasmlar= FileSerializer(many= True, read_only=True)
    mahsulot = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Categoriya
        fields = ['id','categoriya_nomi', 'rasmlar', 'mahsulot' ]