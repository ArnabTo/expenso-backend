from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class FutureAIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"message": "AI Engine feature coming soon."},
            status=501
        )

    def post(self, request):
        return Response(
            {"message": "AI Engine feature coming soon."},
            status=501
        )
