from django.urls import path

from main.views import (
    CreateUserAPIView, LoginUserAPIView, ChangePasswordAPIView, LogoutUserAPIView, CabinetAPIView, PupilsListAPIView,
    AddPupilToTeacherAPIView, SandBoxAPIView, AddClassToTeacherAPIView, AddPupilToClassAPIView, ClassInfoAPIView,
    TeachersPupilsAPIView, ClassesListAPIView, CreateSingleTaskAPIView, SingleTasksListAPIView, TaskToPupilAIView,
    PupilsTasksAPIView, PupilsCurrentTaskAPIView, PupilsSendSolutionAPIView, ProgLanguageAPIView,
    ChangeSingleTaskAPIView, DeletePupilFromTeacher, DeletePupilFromClass, DeleteClassAPIView, TaskToClassAPIView,
    ClassesTaskAPIViews
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
    path('delete_pupil_from_teacher/<int:pupil_id>/', DeletePupilFromTeacher.as_view(), name='delete_pupil'),
    path('delete_pupil_from_class/<int:class_id>/<int:pupil_id>/', DeletePupilFromClass.as_view(),name='delete_pupil_class'),
    path('delete_class/<int:class_id>/', DeleteClassAPIView.as_view(), name='delete_class'),
    path('class_info/<int:class_id>/', ClassInfoAPIView.as_view(), name='class_info'),
    path('classes_list/', ClassesListAPIView.as_view(), name='classes_list'),
    path('single_task/', CreateSingleTaskAPIView.as_view(), name='create_single_task'),
    path('single_task/<int:task_id>/', ChangeSingleTaskAPIView.as_view(), name='change_single_task'),
    path('all_single_tasks/', SingleTasksListAPIView.as_view(), name='list_single_tasks'),
    path('task_to_pupil/<int:task_id>/', TaskToPupilAIView.as_view(), name='task_to_pupil'),
    path('task-to_class/<int:class_id>/<int:task_id>/', TaskToClassAPIView.as_view(),name='task_to_class'),
    path('classes_tasks/<int:class_id>/', ClassesTaskAPIViews.as_view(), name='class_tests'),

    path('pupils_tasks/', PupilsTasksAPIView.as_view(), name='pupils_task'),
    path('pupils_tasks/<int:task_id>/', PupilsCurrentTaskAPIView.as_view(), name='current_task'),
    path('pupils_tasks/<int:task_id>/send_solution/', PupilsSendSolutionAPIView.as_view(), name='send_solution'),
    path('get_languages/', ProgLanguageAPIView.as_view(), name='languages'),
]
