from django.http import HttpResponse


# simple view for uptime robot to ping to keep site active
def monitor_site(requests):
    print("monitor check")
    return HttpResponse("Hello")