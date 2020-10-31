from django.urls import path

from main.views import (
    CreateUserAPIView, LoginUserAPIView, ChangePasswordAPIView, LogoutUserAPIView, CabinetAPIView, PupilsListAPIView,
    AddPupilToTeacherAPIView, SandBoxAPIView
)

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('logout/', LogoutUserAPIView.as_view(), name='logout'),
    path('change_pass/', ChangePasswordAPIView.as_view(), name='change_pass'),
    path('cabinet/', CabinetAPIView.as_view(), name='cabinet'),
    path('pupils/', PupilsListAPIView.as_view(), name='pupil_list'),
    path('add_pupils/', AddPupilToTeacherAPIView.as_view(),name='add_pupils'),
    path('to_sandbox/', SandBoxAPIView.as_view(), name='sandbox'),
]
