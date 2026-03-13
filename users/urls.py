from django.urls import path
from .views import BankBalanceView

urlpatterns = [
    path('bank-balance/', BankBalanceView.as_view(), name='bank-balance'),
]
