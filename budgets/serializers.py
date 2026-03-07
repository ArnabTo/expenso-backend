from rest_framework import serializers
from .models import Budget
from expenses.serializers import CategorySerializer


class BudgetSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    spent = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True, required=False
    )

    class Meta:
        model = Budget
        fields = ('id', 'category', 'category_detail', 'amount', 'month', 'year', 'spent')
        read_only_fields = ('id', 'category_detail', 'spent')
