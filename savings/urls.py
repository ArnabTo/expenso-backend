from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SavingsPlanViewSet, SavingsTransactionViewSet

router = DefaultRouter()
router.register('plans', SavingsPlanViewSet, basename='savings-plan')
router.register('transactions', SavingsTransactionViewSet, basename='savings-transaction')

urlpatterns = [
    path('', include(router.urls)),
]
