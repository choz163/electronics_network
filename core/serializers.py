from rest_framework import serializers
from .models import NetworkNode, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'model', 'release_date')

class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = (
            'id', 'name', 'email', 'country', 'city',
            'street', 'house_number', 'supplier',
            'debt_to_supplier', 'created_at', 'products'
        )
        read_only_fields = ('created_at',)

    def update(self, instance, validated_data):
        validated_data.pop('debt_to_supplier', None)
        return super().update(instance, validated_data)
