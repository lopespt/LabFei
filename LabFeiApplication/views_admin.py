# -*- coding: utf-8 -*-
from django.shortcuts import render

from LabFei.annotations import request_path, check_admin
from LabFeiApplication.forms.LaboratoryDetailsForm import LaboratoryDetailsForm
from LabFeiApplication.models import Laboratory


__author__ = 'wachs'


@request_path("/admin/")
@check_admin
def main(request):
    return render(request, "admin_main.html")

@request_path("/admin/labs")
@check_admin
def labs(request):
    labs_ = Laboratory.objects.all()
    return render(request, "admin_labs.html", {"labs": labs_})

@request_path("/admin/lab_details")
@check_admin
def labs(request):
    lab_id = request.GET['lab_id']
    if lab_id:
        lab = Laboratory.objects.filter(id=lab_id).first()
        if request.method == "POST":
            form = LaboratoryDetailsForm(request.POST, instance=lab)
            if form.is_valid():
                form.save()
        else:
            form = LaboratoryDetailsForm(instance=lab)

        return render(request, "admin_lab_details.html", {"lab": form})