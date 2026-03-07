from django.urls import path
from .views import MonthlyExpenseView, CategoryBreakdownView

urlpatterns = [
    path('monthly-expense/', MonthlyExpenseView.as_view(), name='monthly-expense'),
    path('category-breakdown/', CategoryBreakdownView.as_view(), name='category-breakdown'),
]
