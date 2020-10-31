from main.models import Teacher


class  TeacherMixin(object):

    def __init__(self, request):
        self.teacher = Teacher.objects.get(user=request.user.user2)

    def get_teacher(self):
        return self.teacher
