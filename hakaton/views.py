from rest_framework import views, status
from django.contrib.auth.models import User

class CheckTokenView(views.APIView):
    def get(self, request):
        token = request.GET.get('token')
        if User.objects.filter(auth_token=token):
            return Response({'token': token}, status.HTTP_200_OK)
        return Response({'token': null}, status.HTTP_200_OK)