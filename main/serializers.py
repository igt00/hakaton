from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from main.models import User2, Teacher, Pupil, PupilsClass, CodeTask
from main.validators import validate_password


class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True)
    second_name = serializers.CharField(write_only=True)
    surname = serializers.CharField(write_only=True)
    birthday = serializers.DateField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    is_teacher = serializers.BooleanField(write_only=True)
    auth_token = serializers.CharField(read_only=True)

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
        if validated_data['is_teacher']:
            Teacher.objects.create(user=user.user2)
        else:
            Pupil.objects.create(user=user.user2)

        return user

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


class CabinetSerializer(serializers.ModelSerializer):
    pupil_or_teacher_id = serializers.SerializerMethodField()

    class Meta:
        model = User2
        fields = ['surname', 'first_name', 'second_name', 'gender', 'dt_created', 'email', 'dt_birthday', 'pupil_or_teacher_id']

    def get_pupil_or_teacher_id(self, user):
        if getattr(user, 'pupil', None):
            return user.pupil.id
        return user.teacher.id


class PupilClassSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    pupils = serializers.SerializerMethodField()

    class Meta:
        model = PupilsClass
        fields = ['id', 'title', 'teacher', 'pupils']

    def get_teacher(self, obj):
        teacher = obj.teacher
        return CabinetSerializer(teacher.user).data

    def get_pupils(self, obj):
        return CabinetSerializer(obj.pupils, many=True).data


class SingleTasksListSerializer(serializers.ModelSerializer):
    pupils_count = serializers.SerializerMethodField()

    class Meta:
        model = CodeTask
        fields = ['id', 'name', 'pupils_count']

    def get_pupils_count(self, obj):
        return obj.codepupiltask_set.count()


class PupilTaskListSerializer(serializers.ModelSerializer):
    is_ready = serializers.SerializerMethodField()

    class Meta:
        model = CodeTask
        fields = ['id', 'name', 'is_ready']

    def get_status(self, obj):
        return obj.check_is_ready()


