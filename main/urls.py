from django.urls import path

from main.views import (
    CreateUserAPIView, LoginUserAPIView, ChangePasswordAPIView, LogoutUserAPIView, CabinetAPIView, PupilsListAPIView,
    AddPupilToTeacherAPIView, SandBoxAPIView, AddClassToTeacherAPIView, AddPupilToClassAPIView, ClassInfoAPIView,
    TeachersPupilsAPIView, ClassesListAPIView, CreateSingleTaskAPIView, SingleTasksListAPIView
)

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('logout/', LogoutUserAPIView.as_view(), name='logout'),
    path('change_pass/', ChangePasswordAPIView.as_view(), name='change_pass'),
    path('cabinet/', CabinetAPIView.as_view(), name='cabinet'),
    path('pupils/', PupilsListAPIView.as_view(), name='pupil_list'),
    path('teachers_pupils/', TeachersPupilsAPIView.as_view(), name='teathecrs_pupils'),
    path('add_pupils/', AddPupilToTeacherAPIView.as_view(),name='add_pupils'),
    path('to_sandbox/', SandBoxAPIView.as_view(), name='sandbox'),
    path('add_class/', AddClassToTeacherAPIView.as_view(), name='add_class'),
    path('add_pupils_to_class/<int:class_id>/', AddPupilToClassAPIView.as_view(), name='add_pupils_to_class'),
    path('class_info/<int:class_id>/', ClassInfoAPIView.as_view(), name='class_info'),
    path('classes_list/', ClassesListAPIView.as_view(), name='classes_list'),
    path('single_task/', CreateSingleTaskAPIView.as_view(), name='create_single_task'),
    path('single_tasks/', SingleTasksListAPIView.as_view(), name='list_single_tasks'),
]
