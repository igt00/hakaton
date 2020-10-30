from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from accounts.models import User2
from accounts.validations import validate_password


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        User2.objects.create(user=user)

        return user

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError('Данный email уже занят')

        return email


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20, min_length=6)

    def validate_password(self, password):
        validate_password(password)
        return password