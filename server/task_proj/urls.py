from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse

def connection(request):
    return JsonResponse({"connected":True})

def not_found(request):
    return JsonResponse({"error":"Sorry this endpoint does not exist within this server please check your URL and try again"}, status=404)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/v1/test/', connection),
    path('api/v1/tasks/', include('task_app.urls')),
    path('api/v1/users/', include('user_app.urls')),
    # path('*api/tr')
    re_path(r".*", not_found)
]

"""
. = any character to include special characters
* = 0 or 1 or many instances
g9h8iqrhtfgiaewrtf True
2309482349805rtfvwsrqw True
api/v1/tasts/ True
"""