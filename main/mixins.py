from main.models import Teacher, Pupil


class TeacherMixin(object):

    def get_teacher(self, request):
        return Teacher.objects.get(user=request.user.user2)


class PupilMixin(object):

    def get_pupil(self, request):
        return Pupil.objects.get(user=request.user.user2)
