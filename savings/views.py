from rest_framework import viewsets, permissions
from .models import SavingsPlan, SavingsTransaction
from .serializers import SavingsPlanSerializer, SavingsPlanListSerializer, SavingsTransactionSerializer


class SavingsPlanViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavingsPlan.objects.filter(user=self.request.user).prefetch_related('transactions')

    def get_serializer_class(self):
        if self.action == 'list':
            return SavingsPlanListSerializer
        return SavingsPlanSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavingsTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = SavingsTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = SavingsTransaction.objects.filter(
            plan__user=self.request.user
        ).select_related('plan')

        # Optional filter by plan
        plan_id = self.request.query_params.get('plan')
        if plan_id:
            qs = qs.filter(plan_id=plan_id)

        return qs
