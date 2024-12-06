from django.urls import path
from .views import VerifyCodeView, GenerateVerificationCodeView

urlpatterns = [
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('generate-code/', GenerateVerificationCodeView.as_view(), name='generate-code'),
]
