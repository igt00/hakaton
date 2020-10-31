from rest_framework import views, status
from django.contrib.auth.models import User
from rest_framework.response import Response

class CheckTokenView(views.APIView):
    def get(self, request):
        token = request.GET.get('token')
        user = User.objects.filter(auth_token=token).first()
        if user is not None:
            data = {'token': token}
            if getattr(user, 'teacher', False):
                data['is_teacher'] = True
            elif getattr(user, 'pupil', False):
                data['is_teacher'] = False
            return Response(data, status.HTTP_200_OK)

        return Response({'token': None}, status.HTTP_200_OK)
