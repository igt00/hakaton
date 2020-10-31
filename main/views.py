from rest_framework import views, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

# from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import User2, Teacher, Pupil, PupilsClass, CodeTask, CodePupilTask, TestData, ProgLanguage, CodePupilTaskTry
from main.mixins import TeacherMixin, PupilMixin
from main.serializers import (
    CreateUserSerializer, ChangePasswordSerializer, CabinetSerializer, PupilClassSerializer,
    SingleTasksListSerializer, PupilTaskListSerializer, ProgLanguageSerializer
)
from main.permissons import TeacherPermission, PupilPermission

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
        token = serializer.data['auth_token']
#         print(token)
#         user = User.objects.get(auth_token=token)
#         print(user)
#         user2 = User2.objects.get(user=user)
#         data = {'token_key': token}
#         try:
#             teacher = Teacher.objects.get(user=user2)
#         except:
#             teacher = None
#         try:
#             pupil = Pupil.objects.get(user=user2)
#         except:
#             pupil = None
#         if teacher:
#             data['is_teacher'] = True
#         elif pupil:
#             data['is_teacher'] = False
        return Response(data, status.HTTP_200_OK)


class LoginUserAPIView(views.APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            token = get_object_or_404(Token, user=user).key
            print(token)
            data = {'token_key': token}
            user2 = User2.objects.get(user=user)
            try:
                teacher = Teacher.objects.get(user=user2)
            except:
                teacher = None
            try:
                pupil = Pupil.objects.get(user=user2)
            except:
                pupil = None
            if teacher:
                data['is_teacher'] = True
            elif pupil:
                data['is_teacher'] = False
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutUserAPIView(views.APIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated]

    def get(self,  request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ChangePasswordAPIView(views.APIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated]

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
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated]

    def get(self, request):
        serializer = CabinetSerializer(request.user.user2)
        return Response(serializer.data)

    def put(self, request):
        pass


class PupilsListAPIView(ListAPIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated]
    serializer_class = CabinetSerializer

    def get_queryset(self):
        user_pupil_ids = Pupil.objects.all().values_list('user_id', flat=True)
        return User2.objects.filter(id__in=user_pupil_ids)


class AddPupilToTeacherAPIView(views.APIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated, TeacherPermission]

    def put(self, request):
        teacher = self.get_teacher(request)
        pupils_id = request.data['pupils_id']
        print(pupils_id)
        for pupil in Pupil.objects.filter(id__in=pupils_id):
            teacher.pupil_set.add(pupil)
        teacher.save()
        return Response(status.HTTP_200_OK)


class SandBoxAPIView(views.APIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated]

    def post(self, request):
        code = request.data['code']
        lang = request.data['lang']
        input = request.data['input']
        output = request.data['output']
        runner = Runner(code, lang, 'username', output, input)
        result = runner.run_python()

        print(result)
        return Response(result)


class AddClassToTeacherAPIView(views.APIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated, TeacherPermission]

    def post(self, request):
        teacher = self.get_teacher(request)
        title = request.data['title']
        pupils_class = PupilsClass.objects.create(teacher=teacher, title=title)
        return Response({'id': pupils_class.id}, status.HTTP_201_CREATED)


class AddPupilToClassAPIView(views.APIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated]

    def put(self, request, class_id):
        pupils_id = request.data['pupils_id']
        class_object = PupilsClass.objects.get(pk=class_id)
        class_object.pupils.add(Pupil.objects.filter(pk__in=pupils_id))
        class_object.save()
        return Response(status.HTTP_200_OK)


class ClassInfoAPIView(views.APIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated]

    def get(self, request, class_id):
        class_object = PupilsClass.objects.get(pk=class_id)
        data = {}
        data['title'] = class_object.title
        data['teacher'] = {
            'id': class_object.teacher.user.id,
            'surname': class_object.teacher.user.surname,
            'first_name': class_object.teacher.user.first_name,
            'second_name': class_object.teacher.user.second_name,
        }
        pupils = []
        for pup in class_object.pupils.all():
            pupils.append({
                'id': pup.user.id,
                'surname': pup.user.surname,
                'first_name': pup.user.first_name,
                'second_name': pup.user.second_name,
            })


class TeachersPupilsAPIView(ListAPIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated, TeacherPermission]
    serializer_class = CabinetSerializer

    def get_queryset(self):
        teacher = self.get_teacher(self.request)
        user_pupil_ids = teacher.pupil_set.all().values_list('user_id', flat=True)
        return User2.objects.filter(id__in=user_pupil_ids)


class ClassesListAPIView(ListAPIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated,TeacherPermission]
    serializer_class = PupilClassSerializer

    def get_queryset(self):
        teacher = self.get_teacher(self.request)
        return teacher.pupilsclass_set.all()


class CreateSingleTaskAPIView(views.APIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated, TeacherPermission]

    def post(self, request):
        teacher = self.get_teacher(request)
        data = request.data
        task = CodeTask.objects.create(
            teacher=teacher,
            name=data['name'],
            description=data['descr'],
        )
        for test in data['tests']:
            TestData.objects.create(
                task=task,
                input_data=test['input'],
                output_data=test['output'],
            )
        return Response({'task_id': task.id}, status.HTTP_200_OK)


class SingleTasksListAPIView(ListAPIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated, TeacherPermission]
    serializer_class = SingleTasksListSerializer

    def get_queryset(self):
        teacher = self.get_teacher(self.request)
        return teacher.codetask_set.all()


class TaskToPupilAIView(views.APIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated, TeacherPermission]

    def put(self, request, task_id):
        pupils_id = request.data['pupils_id']
        task = get_object_or_404(CodeTask, pk=task_id)
        for pupil in Pupil.objects.filter(id__in=pupils_id):
            CodePupilTask.objects.create(task=task, pupil=pupil)
        return Response(status.HTTP_201_CREATED)


class PupilsTasksAPIView(PupilMixin, ListAPIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated, PupilPermission]
    serializer_class = PupilTaskListSerializer

    def get_queryset(self):
        pupil = self.get_pupil(self.request)
        return pupil.codepupiltask_set.all()


class PupilsCurrentTaskAPIView(RetrieveAPIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated, PupilPermission]

    def get(self, request, task_id):
        pupil = self.get_pupil(request)
        task = CodeTask.objects.get(pk=task_id)
        pupilcodetask = CodePupilTask.objects.get(pupil=pupil, task=task)
        data = {}
        data['id'] = task.id
        data['name'] = task.name
        data['descr'] = task.description
        data['is_ready'] = pupilcodetask.check_is_ready()
        tries_data = []
        for test in pupilcodetask.get_tries().order_by('-id'):
            tries_data.append({
                'try_status': test.status,
                'tests_count': test.tests_count,
                'failed_tests_count': test.failed_tests_count,
            })
        data['tries_data'] = tries_data
        data['teacher'] = {
            'surname': task.teacher.user.surname,
            'first_name': task.teacher.user.first_name,
            'second_name': task.teacher.user.second_name,
        }
        return Response(data, status.HTTP_200_OK)


class PupilsSendSolutionAPIView(views.APIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated, PupilPermission]

    def post(self, request, task_id):
        pupil = self.get_pupil(request)
        language = get_object_or_404(ProgLanguage, name=request.data['lang'])
        code = request.data['code']
        task = get_object_or_404(CodeTask, pk=task_id)
        input= []
        output = []
        testsdata = task.testdata_set.all()
        input = testsdata.values_list('input_data', flat=True)
        output = testsdata.values_list('output_data', flat=True)
        runner = Runner(code, language.name, request.user.username, output, input)
        result = runner.run_compile()

        print(result['tests'])

        if result['status'] == 'ERROR':
            try_status = 0
            failed_tests_count = None
            tests_count = None
        else:
            try_status = 1
            failed_tests_count = 0
            tests_count = len(result['tests'])
            for test in result['tests']:
                if test == 'ERROR':
                    failed_tests_count += 1

        CodePupilTaskTry.objects.create(
            pupil_task=CodePupilTask.objects.get(task=task, pupil=pupil),
            language=language,
            code=code,
            status=try_status,
            tests_count=tests_count,
            failed_tests_count=failed_tests_count,
        )
        data = {
            'failed_count': failed_tests_count,
            'tests_count': tests_count,
            'tests_score': None if tests_count is None else (tests_count - failed_tests_count) / tests_count * 100,
            'status': try_status,
            'error': result['tests'][0] if try_status == 0 else None
        }
        return Response(data, status.HTTP_200_OK)


class ProgLanguageAPIView(ListAPIView):
    authentication_classes = ()  # [SessionAuthentication]
    permission_classes = ()  # [IsAuthenticated]
    queryset = ProgLanguage.objects.all()
    serializer_class = ProgLanguageSerializer

#
# class ChangeSingleTaskAPIView(PupilMixin, views.APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated, PupilPermission]
#
#     def put(self, request, task_id):
#
#         pass
