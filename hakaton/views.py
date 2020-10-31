from rest_framework import views, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from main.models import User2, Teacher, Pupil

class CheckTokenView(views.APIView):
    def get(self, request):
        token = request.GET.get('token')
        user = User.objects.filter(auth_token=token).first()
        if user is not None:
            data = {'token': token}
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
            return Response(data, status.HTTP_200_OK)

        return Response({'token': None}, status.HTTP_200_OK)
