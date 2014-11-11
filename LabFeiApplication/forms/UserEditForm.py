# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple, TextInput
from django.utils import timezone

from LabFeiApplication.models import User, UserCourses, Course


__author__ = 'wachs'


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'courses']

        widgets = {'courses': CheckboxSelectMultiple(),
                   'name': TextInput(attrs={'size': 40}),
                   'email': TextInput(attrs={'size': 40})}
        labels = {
            'name': 'Nome',
            'email': 'Email',
            'courses': 'Cursos',
        }

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        def nome_curso(obj):
            return obj.name + " [%s]" % obj.code

        self.fields['courses'].label_from_instance = nome_curso

    def save(self, commit=True):
        self.is_valid()
        if 'courses' in self.cleaned_data:
            courses_db = self.cleaned_data['courses']
            UserCourses.objects.filter(user__id=self.instance.id).exclude(
                course__in=[c.id for c in courses_db]).delete()
            for course in courses_db:
                if UserCourses.objects.filter(course__id=course.id, user__id=self.instance.id).count() == 0:
                    uc = UserCourses(user=self.instance, course=Course.objects.filter(id=course.id).first(),
                                     subscriptionDate=timezone.now())
                    uc.save()
        else:
            UserCourses.objects.filter(user__id=self.instance.id).delete()
        self.instance.save()


