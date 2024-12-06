
from django.urls import path, include

urlpatterns = [
    path("api/sms/", include("sms.urls")),
    path("api/user/", include("user_management.urls")),
]
