from rest_framework import serializers
from .models import SavingsPlan, SavingsTransaction


class SavingsTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsTransaction
        fields = ('id', 'plan', 'amount', 'date', 'note', 'created_at')
        read_only_fields = ('id', 'created_at')


class SavingsPlanSerializer(serializers.ModelSerializer):
    transactions = SavingsTransactionSerializer(many=True, read_only=True)
    total_saved = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = SavingsPlan
        fields = (
            'id', 'name', 'description', 'target_amount', 'monthly_deposit',
            'start_date', 'end_date', 'is_active', 'created_at',
            'total_saved', 'progress_percentage', 'transactions',
        )
        read_only_fields = ('id', 'created_at', 'total_saved', 'progress_percentage')


class SavingsPlanListSerializer(serializers.ModelSerializer):
    """Lightweight list serializer without transactions."""
    total_saved = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = SavingsPlan
        fields = (
            'id', 'name', 'description', 'target_amount', 'monthly_deposit',
            'start_date', 'end_date', 'is_active', 'created_at',
            'total_saved', 'progress_percentage',
        )
        read_only_fields = ('id', 'created_at')
