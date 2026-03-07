from django.urls import path
from .views import MonthlyReportView, YearlyReportView

urlpatterns = [
    path('monthly/', MonthlyReportView.as_view(), name='monthly-report'),
    path('yearly/', YearlyReportView.as_view(), name='yearly-report'),
]
