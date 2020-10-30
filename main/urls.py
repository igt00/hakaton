from django.urls import path

from main.views import (
    CreateUserAPIView, LoginUserAPIView, ChangePasswordAPIView, LogoutUserAPIView, #CabinetAPIView
)

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('logout/', LogoutUserAPIView.as_view(), name='logout'),
    path('change_pass/', ChangePasswordAPIView.as_view(), name='change_pass'),
#     path('cabinet/', CabinetAPIView.as_views(), name='cabinet'),
]