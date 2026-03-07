from rest_framework import serializers
from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'icon', 'color', 'is_default')
        read_only_fields = ('id',)


class ExpenseSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Expense
        fields = (
            'id', 'title', 'amount', 'date', 'note',
            'category', 'category_detail', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'category_detail')
