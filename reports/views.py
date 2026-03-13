from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from expenses.models import Expense
from budgets.models import Budget
from savings.models import SavingsTransaction


class MonthlyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if not year or not month:
            return Response({"error": "year and month are required"}, status=400)

        # 1. Expenses
        expenses_total = Expense.objects.filter(
            user=request.user, date__year=year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        # 2. Budgets
        budget_total = Budget.objects.filter(
            user=request.user, year=year, month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        # 3. Savings (deposits this month)
        savings_total = SavingsTransaction.objects.filter(
            plan__user=request.user, date__year=year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "year": year,
            "month": month,
            "summary": {
                "total_expenses": float(expenses_total),
                "total_budgeted": float(budget_total),
                "total_saved": float(savings_total),
                "bank_balance": float(request.user.bank_balance),
                "budget_utilized_percentage": round(
                    (float(expenses_total) / float(budget_total) * 100), 1
                ) if budget_total else 0
            }
        })


class YearlyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year')
        if not year:
            return Response({"error": "year is required"}, status=400)

        # Basic aggregation by month (could also use TruncMonth)
        monthly_expenses = Expense.objects.filter(
            user=request.user, date__year=year
        ).values('date__month').annotate(total=Sum('amount')).order_by('date__month')

        monthly_savings = SavingsTransaction.objects.filter(
            plan__user=request.user, date__year=year
        ).values('date__month').annotate(total=Sum('amount')).order_by('date__month')

        return Response({
            "year": year,
            "expenses_by_month": list(monthly_expenses),
            "savings_by_month": list(monthly_savings)
        })
