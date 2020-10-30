from django.db import models

from main.choices import GENDER_CHOICES

class User2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=40, verbose_name='Фамилия')
    first_name = models.CharField(max_length=40, verbose_name='Имя')
    second_name = models.CharField(max_length=40, verbose_name='Отчество', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол', blank=True, null=True)
    dt_created = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True)
    email = models.CharField(max_length=50, verbose_name='Мейл', unique=True)
    dt_birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')


class Teacher(models.Model):
    user2 = models.ForeignKey(User2, on_delete=models.CASCADE, verbose_name='Пользователь-учитель')


class Pupil(models.Model):
    user2 = models.ForeignKey(User2, on_delete=models.CASCADE, verbose_name='Пользователь-ученик')


class CodeTask(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Учитель')
    description = models.TextField()


class CodePupilTask(models.Model):
    task = models.ForeignKey(CodeTask, on_delete=models.CASCADE)
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE)


class ProgLanguage(models.Model):
    name = models.CharField(max_length=30, verbose_name='Язык программирования')
    translit = models.CharField(max_length=30, verbose_name='Транслит', null=True, blank=True)


class CodePupilTaskTry(models.Model):
    pupil_task = models.ForeignKey(CodePupilTask, on_delete=models.CASCADE)
    language = models.ForeignKey(ProgLanguage, on_delete=models.CASCADE)
    code = models.TextField(verbose_name='Код ученика')

# class CodeTaskFile(models.Model):
#     file_m = models.FileField()
#     file_l = models.FileField()
#     task = models.ForeignKey(CodeTask, on_delete=models.CASCADE)
