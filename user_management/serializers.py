from rest_framework import serializers
from .models import User, VerificationCode

class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = ['id', 'user', 'code', 'expiration_time']


class UserSerializer(serializers.ModelSerializer):
    verification_code = VerificationCodeSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'name', 'last_name', 'avatar_link', 'email',
            'phone_number', 'status', 'jwt_token', 'verification_code'
        ]
