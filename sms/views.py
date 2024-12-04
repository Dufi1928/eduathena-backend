from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client
from rest_framework import status

class SendSMSView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        message = request.data.get("message")

        if not phone_number or not message:
            return Response({"error": "Numéro de téléphone et message requis."}, status=status.HTTP_400_BAD_REQUEST)

        # Initialisez le client Twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        try:
            # Envoyez le SMS
            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            return Response({"success": "Message envoyé avec succès."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
