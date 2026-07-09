from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import datetime

class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self,request, *args, **kwargs):
        return Response(
            {
            "status":"ok",
            "timestamp": datetime.now().isoformat(),
            }
        )
