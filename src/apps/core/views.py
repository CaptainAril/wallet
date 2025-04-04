from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheck(APIView):
    def get(self, request, *args, **kwargs):
        return Response(data={
            "success": True,
            "message": "Server is running"
        }, status=status.HTTP_200_OK)