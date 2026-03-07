from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Sum, Q
from expenses.models import Expense
from .models import Budget
from .serializers import BudgetSerializer


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Budget.objects.filter(user=self.request.user).select_related('category')
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        if month:
            queryset = queryset.filter(month=month)
        if year:
            queryset = queryset.filter(year=year)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        budgets_with_spent = []
        for budget in queryset:
            spent = Expense.objects.filter(
                user=request.user,
                category=budget.category,
                date__month=budget.month,
                date__year=budget.year,
            ).aggregate(total=Sum('amount'))['total'] or 0

            data = BudgetSerializer(budget).data
            data['spent'] = float(spent)
            data['remaining'] = float(budget.amount) - float(spent)
            data['percentage'] = round((float(spent) / float(budget.amount)) * 100, 1) if budget.amount else 0
            budgets_with_spent.append(data)

        return Response(budgets_with_spent)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
