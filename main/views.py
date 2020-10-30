from rest_framework import views, status
from rest_framework.generics import CreateAPIView

from django.contrib.auth import authenticate, login, logout

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import User2
from main.serializers import CreateUserSerializer, ChangePasswordSerializer


class CreateUserAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = CreateUserSerializer


class LoginUserAPIView(views.APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutUserAPIView(views.APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,  request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ChangePasswordAPIView(views.APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.data['password'])
        user.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return Response(status=status.HTTP_200_OK)


# def ProfileAPIView(views.APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         user2 = request.user.user2
#         is_teacher = Teacher.objects.filter(user=user2).first()
#         is_pupil = Pupil.objects.filter(user=user2).first()
