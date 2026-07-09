from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import datetime
from django.db import connections
from django_redis import get_redis_connection
from celery import current_app

class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self,request, *args, **kwargs):
        health_data = {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "database": self._check_database(),
                "redis": self._check_redis(),
                "celery": self._check_celery()
            }
        }
        if any(v != "ok" for v in health_data["services"].values()):
            health_data["status"] = "degraded"
        return Response(health_data)

    def _check_database(self):
        try:
            connections["default"].cursor()
            return "ok"
        except Exception as e:
            return f"error: {e}"

    def _check_redis(self):
        try:
            r = get_redis_connection("default")
            r.ping()
            return "ok"
        except Exception as e:
            return f"error: {e}"

    def _check_celery(self):
        try:
            inspect = current_app.control.inspect()
            stats = inspect.ping()
            if stats:
                return "ok"
            return "no workers"
        except Exception as e:
            return f"error: {e}"