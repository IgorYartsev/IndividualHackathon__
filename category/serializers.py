from rest_framework import serializers
from .models import Category



class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields= ('name',)

class CategoryDetailSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'