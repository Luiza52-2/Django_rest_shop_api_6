from rest_framework import serializers
from .models import CustomUser as User
from rest_framework.exceptions import ValidationError
from django.core.cache import cache

from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer

class UserBaseSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)



class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):
    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except:
            return email
        raise ValidationError('Email уже существует!')


class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        code = attrs.get('code')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError('User не существует!')

        redis_key = f'user_confirmation_code_{user.email}'
        stored_code = cache.get(redis_key)


        if stored_code is None:
            raise ValidationError('Код не найден или истек!')
        
        if stored_code != code:
            raise ValidationError('Неверный код подтверждения!')
        cache.delete(redis_key)

        return attrs
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['birthday'] = str(user.birthday) if user.birthday else None
        return token


class GoogleLoginSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)