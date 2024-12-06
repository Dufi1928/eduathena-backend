import random
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client
from rest_framework import status

class SendSMSView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")

        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        verification_code = random.randint(1000, 9999)

        message = f"Yor verification code is  : {verification_code}"

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        try:
            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            return Response({"success": "Message sent successfully.", "code": verification_code}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
