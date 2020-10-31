from main.models import Teacher, Pupil


class TeacherMixin(object):

    def get_teacher(self, request):
        return Teacher.objects.get(user=request.user.user2)


class PupilMixin(object):

    def __init__(self, request):
        self.pupil = Pupil.objects.get(user=request.user.user2)

    def get_teacher(self):
        return self.pupil
