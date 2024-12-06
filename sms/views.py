from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from twilio.rest import Client




class SendSMSView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        message = request.data.get("message")

        if not phone_number or not message:
            return Response({"error": "Phone number and message are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            send_sms(phone_number, message)
            return Response({"success": "Message sent successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to send SMS: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def send_sms(phone_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
    except Exception as e:
        raise Exception(f"Failed to send SMS: {str(e)}")

