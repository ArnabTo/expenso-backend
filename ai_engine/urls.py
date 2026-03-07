from django.urls import path
from .views import FutureAIView

urlpatterns = [
    path('', FutureAIView.as_view(), name='ai-engine-placeholder'),
]
