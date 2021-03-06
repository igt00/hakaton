from django.db import models
from django.contrib.auth.models import User

from main.choices import GenderChoice

class User2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=40, verbose_name='Фамилия')
    first_name = models.CharField(max_length=40, verbose_name='Имя')
    second_name = models.CharField(max_length=40, verbose_name='Отчество', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GenderChoice.GENDER_CHOICES, verbose_name='Пол', blank=True, null=True)
    dt_created = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True)
    email = models.CharField(max_length=50, verbose_name='Мейл', unique=True)
    dt_birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')


class Teacher(models.Model):
    user = models.OneToOneField(User2, on_delete=models.CASCADE)


class Pupil(models.Model):
    user = models.OneToOneField(User2, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(Teacher, null=True, blank=True)


class PupilsClass(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    pupils = models.ManyToManyField(Pupil, null=True, blank=True)
    title = models.CharField(max_length=30)


class Course(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название курса')
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, verbose_name='Пользователь в роли учителя')
    description = models.TextField()


class Lesson(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название урока')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс к которому относится урок')
    description = models.TextField()


class CodeTask(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название задачи')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Пользователь в роли учителя')
    description = models.TextField()
    task_to_class = models.BooleanField(default=False)
    pupilclass = models.ForeignKey(PupilsClass, null=True,on_delete=models.CASCADE)

    def get_tasks_pupil(self):
        return self.codepupiltask_set.all()

    def get_tasks_pupil_count(self):
        return self.get_tasks_pupil().count()


class CodeToLesson(models.Model):
    task = models.ForeignKey(CodeTask, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок к которому относится задача')


class TestData(models.Model):
    task = models.ForeignKey(CodeTask, on_delete=models.CASCADE)
    input_data = models.CharField(max_length=64, verbose_name='Входные данные', null=True)
    output_data = models.CharField(max_length=64, verbose_name='Выходные данные', null=True)


class CodePupilTask(models.Model):
    task = models.ForeignKey(CodeTask, on_delete=models.CASCADE)
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, verbose_name='Пользователь в роли ученика')
    task_to_class = models.BooleanField(default=False)

    def get_tries(self):
        return self.codepupiltasktry_set.all()

    def check_is_ready(self):
        return self.get_tries().filter(failed_tests_count=0).exists()

    def get_count_tries(self):
        return self.get_tries().count()


class ProgLanguage(models.Model):
    name = models.CharField(max_length=30, verbose_name='Язык программирования')
    translit = models.CharField(max_length=30, verbose_name='Транслит', null=True, blank=True)


class CodePupilTaskTry(models.Model):
    pupil_task = models.ForeignKey(CodePupilTask, on_delete=models.CASCADE)
    language = models.ForeignKey(ProgLanguage, on_delete=models.CASCADE)
    code = models.TextField(verbose_name='Код ученика')
    status = models.CharField(max_length=1, verbose_name='Успешность выполнения')
    tests_count = models.IntegerField(null=True)
    failed_tests_count = models.IntegerField(null=True)


# class CodeTaskFile(models.Model):
#     file_m = models.FileField()
#     file_l = models.FileField()
#     task = models.ForeignKey(CodeTask, on_delete=models.CASCADE)
