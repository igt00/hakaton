from main.models import Teacher


class  TeacherMixin(object):

    def get_teacher(self, request):
        return Teacher.objects.get(user=request.user.user2)
