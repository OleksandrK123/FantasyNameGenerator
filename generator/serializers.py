from rest_framework import serializers
from .models import FantasyName, NameCategory


class FantasyNameSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = FantasyName
        fields = ['id', 'name', 'category_name', 'created_at']
