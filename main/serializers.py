from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from main.models import User2
from main.validators import validate_password


class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    second_name = serializers.CharField()
    surname = serializers.CharField()
    birthday = serializers.DateField()
    password = serializers.CharField()
    email = serializers.CharField()

    def create(self, validated_data):
        user = User(
            username=validated_data['email'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        User2.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            second_name=validated_data['second_name'],
            surname=validated_data['surname'],
            dt_birthday=validated_data['birthday'],
            email=validated_data['email'],
        )

        return token

#     def validate_password(self, password):
#         validate_password(password)
#         return password

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError('Данный email уже занят')

        return email


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20, min_length=6)

#     def validate_password(self, password):
#         validate_password(password)
#         return password