from main.models import Pupil, CodeTask, CodePupilTask, CodePupilTaskTry

def count_pupil_score(task, pupil):
    codepupiltask = CodePupilTask.objects.get(pupil=pupil, task=task)
    tring_count = codepupiltask.codepupiltasktry_set.count()
    if 0 <= tring_count <= 2:
        return 5
    elif 3 <= tring_count <= 6:
        return 4
    elif 7 <= tring_count <= 10:
        return 3
    return 2
