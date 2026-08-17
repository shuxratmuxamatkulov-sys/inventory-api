from rest_framework import serializers
from .models import Category, Product, Transaction

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = ['id', 'category', 'category_name', 'name', 'quantity', 'price', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Transaction
        fields = ['id', 'product', 'product_name', 'user', 'user_username', 'type', 'quantity', 'note', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        # Transaction yaratilganda mahsulot qoldig'ini avtomatik yangilash
        product = validated_data['product']
        quantity = validated_data['quantity']
        trans_type = validated_data['type']

        if trans_type == 'IN':
            product.quantity += quantity
        elif trans_type == 'OUT':
            if product.quantity < quantity:
                raise serializers.ValidationError({"quantity": "Omborda yetarli mahsulot mavjud emas!"})
            product.quantity -= quantity

        product.save()
        return super().create(validated_data)