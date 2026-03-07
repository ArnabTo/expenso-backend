from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from expenses.models import Expense

class MonthlyExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if not year or not month:
            return Response({"error": "year and month are required"}, status=400)

        total = Expense.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Optional: daily breakdown
        daily = Expense.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month
        ).values('date').annotate(total=Sum('amount')).order_by('date')

        return Response({
            "year": year,
            "month": month,
            "total_spent": float(total),
            "daily_breakdown": list(daily)
        })

class CategoryBreakdownView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        
        qs = Expense.objects.filter(user=request.user)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        elif year:
            qs = qs.filter(date__year=year)

        breakdown = qs.values(
            'category__id', 'category__name', 'category__color'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')

        return Response(list(breakdown))
