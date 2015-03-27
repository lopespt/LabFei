# -*- coding: utf-8 -*-
import uuid
from zipfile import ZipFile

from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils import timezone

from LabFei import settings
from LabFei.annotations import request_path, check_logged
from LabFeiApplication.models import Laboratory, Course, LaboratorySubmission, CorrectionErrors
from LabFeiApplication.services import userService, labService


__author__ = 'wachs'


@request_path('/user/{login}/labs/')
@check_logged
def main(request, login):
    user = userService.get_logged_user(request)
    courses = user.courses.all()

    course_id = request.GET['course_id'] if 'course_id' in request.GET else None
    if course_id:
        labs = Laboratory.objects.filter(course__id__in=[c.id for c in user.courses.all()]).filter(
            course__id__in=course_id)
        selected_course = Course.objects.filter(id=course_id).first()
    elif user.courses.first() is not None:
        labs = Laboratory.objects.filter(course__id=user.courses.first().id)
        selected_course = Course.objects.filter(id=user.courses.first().id).first()
    else:
        labs = None
        selected_course = None

    return render(request, "labs_main.html", {'labs': labs, 'courses': courses,
                                              'selected_course': selected_course})


class MultiFileInput(forms.FileInput):
    def render(self, name, value, attrs={}):
        attrs['multiple'] = 'multiple'
        return super(MultiFileInput, self).render(name, None, attrs=attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        else:
            return [files.getlist(name)]


class MultiFileField(forms.FileField):
    widget = MultiFileInput
    default_error_messages = {
        'min_num': u"Ensure at least %(min_num)s files are uploaded (received %(num_files)s).",
        'max_num': u"Ensure at most %(max_num)s files are uploaded (received %(num_files)s).",
        'file_size': u"File: %(uploaded_file_name)s, exceeded maximum upload size."
    }

    def __init__(self, *args, **kwargs):
        self.min_num = kwargs.pop('min_num', 0)
        self.max_num = kwargs.pop('max_num', None)
        self.maximum_file_size = kwargs.pop('maximum_file_size', None)
        super(MultiFileField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        ret = []
        for item in data:
            ret.append(super(MultiFileField, self).to_python(item))
        return ret

    def validate(self, data):
        super(MultiFileField, self).validate(data)
        num_files = len(data)
        if len(data) and not data[0]:
            num_files = 0
        if num_files < self.min_num:
            raise ValidationError(self.error_messages['min_num'] % {'min_num': self.min_num, 'num_files': num_files})
            return
        elif self.max_num and num_files > self.max_num:
            raise ValidationError(self.error_messages['max_num'] % {'max_num': self.max_num, 'num_files': num_files})
        for uploaded_file in data:
            if uploaded_file.size > self.maximum_file_size:
                raise ValidationError(self.error_messages['file_size'] % {'uploaded_file_name': uploaded_file.name})


class uploadForm(forms.Form):
    file_upload = MultiFileField()


@request_path('/user/{login}/labs/{lab_id}/')
@check_logged
def lab_details(request, login, lab_id):
    lab = labService.lab_details(request, lab_id)

    if request.method == 'POST':
        file_list = request.FILES.getlist('file_upload')
        file_name = '%s%s.zip' % (settings.SUBMISSION_FOLDER, str(uuid.uuid4()))
        with ZipFile(file_name, 'w') as f:
            for afile in file_list:
                count = float(0.0)
                chunks = afile.chunks()
                for c in chunks:
                    f.writestr(afile.name, c)
                    count += len(c)
        labService.insertSubmission(timezone.now(), file_name, "", userService.get_logged_user(request), lab)

    form = uploadForm()
    if not lab:
        raise RuntimeError('Incorrect lab_id')

    submissions = lab.laboratorysubmission_set.filter(user__id=userService.get_logged_user(request).id).order_by('-id')

    return render(request, "labs_details.html", {'lab': lab, 'form': form, 'submissions': submissions})

@request_path('/user/{login}/labs/{lab_id}/correction_result_ajax')
def lab_correction_details_ajax(request, login, lab_id):
    submission_id = request.GET['submission_id']

    #errors = CorrectionErrors.objects.filter(laboratorySubmission__id=submission_id).filter(laboratorySubmission__user__login=login).all()
    errors = CorrectionErrors.objects.filter(laboratorySubmission__id=submission_id).all()

    return render(request, "labs_correction_ajax.html", { "errors": errors})
