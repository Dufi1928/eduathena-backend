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
            return Response({"error": "Numéro de téléphone requis."}, status=status.HTTP_400_BAD_REQUEST)

        # Générer un code de vérification à 4 chiffres
        verification_code = random.randint(1000, 9999)

        # Créer le message à envoyer par SMS
        message = f"Votre code de vérification est : {verification_code}"

        # Initialisez le client Twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        try:
            # Envoyez le SMS
            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            # Retourner le succès avec le code (évitez d'inclure le code dans un vrai environnement)
            return Response({"success": "Message envoyé avec succès.", "code": verification_code}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
