from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ExpenseViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', include(router.urls)),
]
