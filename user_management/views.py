from twilio.rest import Client
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from eduathena_backend import settings
from .models import User
from .serializers import UserSerializer
from sms.views import send_sms

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        user.generate_verification_code()

        # Send the verification code via SMS
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        try:
            client.messages.create(
                body=f"Your 4-digit verification code is: {user.verification_code}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=user.phone_number
            )
        except Exception as e:
            return Response({"error": f"Failed to send SMS: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Generate a JWT token for the user
        refresh = RefreshToken.for_user(user)
        user.jwt_token = str(refresh.access_token)
        user.save()


class UserDetailByEmailView(APIView):
    @staticmethod
    def get(request, email):
        try:
            user = User.objects.get(email=email)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class VerifyCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        verification_code = request.data.get("verification_code")

        if not phone_number or not verification_code:
            return Response({"error": "Phone number and verification code are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)

            if user.status:
                return Response({"message": "User is already verified."}, status=status.HTTP_200_OK)

            if user.verification_code == verification_code:
                user.status = True
                user.verification_code = None
                user.attempts = 3
                user.save()
                return Response({"success": "User verified successfully."}, status=status.HTTP_200_OK)
            else:
                # Réduire les tentatives restantes
                user.attempts -= 1
                user.save()
                if user.attempts <= 0:
                    return Response({"error": "Maximum attempts reached. Please request a new verification code."}, status=status.HTTP_403_FORBIDDEN)
                return Response({"error": f"Invalid verification code. {user.attempts} attempts remaining."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)



class GenerateVerificationCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")

        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)

            user.generate_verification_code()

            message = f"Your verification code is: {user.verification_code}"
            send_sms(user.phone_number, message)

            return Response({"success": "Verification code sent successfully."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class RegisterUserView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")

        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(phone_number=phone_number)

        if not created and user.status:
            return Response({"error": "This phone number is already registered and verified."}, status=status.HTTP_400_BAD_REQUEST)

        user.generate_verification_code()

        message = f"Your verification code is: {user.verification_code}"
        try:
            send_sms(phone_number, message)
        except Exception as e:
            return Response({"error": f"Failed to send SMS: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"success": "Verification code sent successfully."}, status=status.HTTP_200_OK)