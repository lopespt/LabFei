# -*- coding: utf-8 -*-
from django.core import mail

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple, TextInput, PasswordInput
from django.shortcuts import render
from django.utils import timezone

from LabFeiApplication.models import User, UserCourses, Course


__author__ = 'wachs'


class UserCreateForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'login', 'password', 'courses']

        widgets = {'courses': CheckboxSelectMultiple(),
                   'name': TextInput(attrs={'size': 40}),
                   'email': TextInput(attrs={'size': 40}),
                   'password': PasswordInput()}
        labels = {
            'name': 'Nome',
            'email': 'Email',
            'courses': 'Cursos',
            'login': 'Login',
            'password': 'Senha'
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 5:
            raise ValidationError(
                [ValidationError('A senha deve conter pelo menos 5 letras ou dígitos')]
            )
        return password

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(login=login).exists():
            raise ValidationError('O login já existe na base de dados')

        return login

    def clean_email(self):
        email = self.cleaned_data['email']
        val = EmailValidator(message="E-Mail inválido")
        val(email)
        return email

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        def nome_curso(obj):
            return obj.name + " [%s]" % obj.code

        self.fields['courses'].label_from_instance = nome_curso
        self.fields['courses'].required = False
        for f in self.fields:
            self.fields[f].error_messages['required'] = 'Campo obrigatório'



    def save(self, commit=True):
        self.is_valid()
        if self.instance.role is None:
            self.instance.role = 0

        self.instance.save()

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


