from django.contrib import admin
from django.urls import path, include
from hakaton.views import CheckTokenView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('check_token/', CheckTokenView.as_view(), name='check_token'),
]
