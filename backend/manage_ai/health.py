from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse


def health_view(request):
    return JsonResponse({"status": "ok", "service": "ManageAI API"})


def readiness_view(request):
    checks = {"database": "ok"}
    status = 200
    try:
        connections["default"].cursor().execute("SELECT 1")
    except OperationalError as exc:
        checks["database"] = str(exc)
        status = 503
    return JsonResponse({"status": "ok" if status == 200 else "error", "checks": checks}, status=status)
