from django.urls import path
from .views import SendSMSView

urlpatterns = [
    path('send-sms/', SendSMSView.as_view(), name='send-sms'),
]
