import _thread

from LabFeiApplication.models import Laboratory, LaboratorySubmission
from LabFeiApplication.services import userService, correctionService


__author__ = 'wachs'


def lab_details(request, lab_id):
    user = userService.get_logged_user(request)
    return Laboratory.objects.filter(id=lab_id, course__id__in=[c.id for c in user.courses.all()]).first()


def insertSubmission(date, file_name, status, user, lab):
    sub = LaboratorySubmission()
    sub.dateSubmitted = date
    sub.zippedFile = file_name
    sub.status = status
    sub.user = user
    sub.laboratory = lab
    sub.save()
    thread.start_new_thread(correctionService.start_correction, (sub,))
    #correctionService.start_correction(sub)
