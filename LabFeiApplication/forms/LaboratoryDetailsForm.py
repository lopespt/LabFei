# -*- coding: utf-8 -*-
from django import forms

from LabFeiApplication.models import Laboratory


__author__ = 'wachs'


class LaboratoryDetailsForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = ['title', 'course', 'description', 'mainReplacement']

    def __init__(self, *args, **kwargs):
        super(LaboratoryDetailsForm, self).__init__(*args, **kwargs)

        def nome_curso(obj):
            return obj.name

        self.fields['course'].label_from_instance = nome_curso


