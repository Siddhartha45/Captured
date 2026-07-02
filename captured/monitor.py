from django.http import HttpResponse, JsonResponse
from django.db import connection


# simple view for uptime robot to ping to keep site active
def monitor_site(requests):
    print("monitor check")
    return HttpResponse("Hello")


# hits db to keep it active in aiven
def health_check(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return JsonResponse({"status": "ok"})