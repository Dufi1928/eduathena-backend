from django.urls import path
from .views import VerifyCodeView, GenerateVerificationCodeView, RegisterUserView

urlpatterns = [
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('generate-code/', GenerateVerificationCodeView.as_view(), name='generate-code'),
    path('register/', RegisterUserView.as_view(), name='register'),
]
