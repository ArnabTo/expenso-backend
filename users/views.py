from decimal import Decimal, InvalidOperation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class BankBalanceView(APIView):
    """Get or update the authenticated user's bank balance."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'bank_balance': float(request.user.bank_balance)})

    def patch(self, request):
        raw = request.data.get('bank_balance')
        if raw is None:
            return Response({'error': 'bank_balance is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            balance = Decimal(str(raw))
        except (InvalidOperation, ValueError):
            return Response({'error': 'Invalid bank_balance value'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.bank_balance = balance
        request.user.save(update_fields=['bank_balance'])
        return Response({'bank_balance': float(request.user.bank_balance)})
