# -*- coding: utf-8 -*-

from django.core import mail
from django.shortcuts import render
from django.template.loader import render_to_string

from LabFei.annotations import request_path, check_logged
from LabFeiApplication.forms.UserCreateForm import UserCreateForm
from LabFeiApplication.forms.UserEditForm import UserEditForm

from LabFeiApplication.models import User


__author__ = 'wachs'


@request_path('/user/{login}/')
def main(request, login):
    return render(request, "user_main.html")


@request_path('/user/{login}/edit')
@check_logged
def edit(request, login):
    user = User.objects.filter(login=login).first()

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        form.save()

    form = UserEditForm(instance=user)
    return render(request, 'user_edit.html', {'form': form})


@request_path('/user/create')
def create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():

            connection = mail.get_connection(host='smtp.gmail.com', port=587,
                                             username='guilhermewachs@gmail.com',
                                             password='Cessna080', use_tls=True)
            connection.open()

            msg = mail.EmailMessage("Assunto",
                              render_to_string("email_user_created.html", dictionary={"user": form.instance}),
                              "guilhermewachs@gmail.com", ['guilhermewachs@gmail.com'], connection=connection)
            msg.content_subtype = "html"
            msg.send()

            connection.close()
            form.save()

        else:
            return render(request, "user_create.html", {'form': form})

    form = UserCreateForm()
    return render(request, "user_create.html", {'form': form})