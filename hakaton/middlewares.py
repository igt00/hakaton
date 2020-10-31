from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User

class UserToRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.headers.get('Authorization')
        if token:
            request.user = User.objects.get(auth_token=token)
        return None
