from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F
from django.contrib.auth import get_user_model
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer

User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return default categories + user's custom categories
        return Category.objects.filter(
            Q(is_default=True) | Q(created_by=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'note', 'category__name']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        queryset = Expense.objects.filter(
            user=self.request.user).select_related('category')
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        category = self.request.query_params.get('category')
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if category:
            queryset = queryset.filter(category_id=category)
        if month and year:
            queryset = queryset.filter(date__month=month, date__year=year)
        elif year:
            queryset = queryset.filter(date__year=year)
        return queryset

    def perform_create(self, serializer):
        expense = serializer.save(user=self.request.user)
        User.objects.filter(pk=self.request.user.pk).update(
            bank_balance=F('bank_balance') - expense.amount
        )

    def perform_update(self, serializer):
        old_amount = serializer.instance.amount
        expense = serializer.save()
        diff = expense.amount - old_amount
        if diff != 0:
            User.objects.filter(pk=self.request.user.pk).update(
                bank_balance=F('bank_balance') - diff
            )

    def perform_destroy(self, instance):
        User.objects.filter(pk=self.request.user.pk).update(
            bank_balance=F('bank_balance') + instance.amount
        )
        instance.delete()
