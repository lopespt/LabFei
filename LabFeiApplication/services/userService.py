from django.contrib import sessions
from LabFeiApplication.models import User

__author__ = 'wachs'


def do_login(request):
    login = request.POST.get('login')
    password = request.POST.get('senha')

    user = User.objects.filter(login=login).filter(password=password).first()
    if user is not None:
            request.session['logged_user'] = {'id': user.id, 'login': user.login, 'name': user.name, 'role': user.role}


    return user


def do_logout(request):
    request.session.clear()
    request.session.delete()


def get_logged_user(request):
    return User.objects.filter(id=request.session['logged_user']['id']).first()



