from rest_framework import views, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import User2, Teacher, Pupil
from main.serializers import CreateUserSerializer, ChangePasswordSerializer, CabinetSerializer

from sandbox.authotestlib import Runner

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class CreateUserAPIView(views.APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'token_key': serializer.data['auth_token']}, status.HTTP_200_OK)


class LoginUserAPIView(views.APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            token = get_object_or_404(Token, user=user)
            return Response({'token_key': token.key}, status=status.HTTP_200_OK)
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


class CabinetAPIView(views.APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CabinetSerializer(request.user.user2)
        return Response(serializer.data)

    def put(self, request):
        pass


class PupilsListAPIView(ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CabinetSerializer

    def get_queryset(self):
        user_pupil_ids = Pupil.objects.all().values_list('user_id', flat=True)
        return User2.objects.filter(id__in=user_pupil_ids)


class AddPupilToTeacherAPIView(views.APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        teacher = Teacher.objects.get(user=request.user.user2)
        pupils_id = request.data['pupils_id']
        teacher.pupil_id.add(Pupil.objects.filter(id__in=pupils_id))
        teacher.save()
        return Response(status.HTTP_200_OK)


class SandBoxAPIView(views.APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated]

    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        code = request.data['code']
        lang = request.data['lang']
        input = request.data['input']
        output = request.data['output']
        runner = Runner(code, lang, 'username', output, input)
        result = runner.run_python()

        print(result)
        return Response(result)







