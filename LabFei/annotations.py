# -*- coding: utf-8 -*-
from LabFeiApplication.services import sessionService

__author__ = 'wachs'

# decorators.py
from django.conf import settings
from django.utils.importlib import import_module
from django.conf.urls import patterns, url


def request_path(path):
    path = path.replace("{", "(?P<")
    path = path.replace("}", ">[\w\-_]*)")
    path = r'^%s$' % path[1:]  # Add delimiters and remove opening slash

    print("registrado path - [" + path + "]")

    def decorator(view):
        urls = import_module(settings.ROOT_URLCONF)
        urls.urlpatterns += patterns('', url(path, view))
        return view

    return decorator


class UserNotLogged(RuntimeError):
    pass


def check_logged(f):
    def wrapped(*args, **kwargs):
        request = args[0]
        if 'logged_user' not in request.session:
            raise UserNotLogged('Usuário não logado ou sessão vencida')

        if 'login' in kwargs:
            if request.session['logged_user']['login'] == kwargs['login']:

                return f(*args, **kwargs)
            else:
                raise UserNotLogged('Usuário com credenciais diferentes')

        return f(*args, **kwargs)

    return wrapped


def check_admin(f):
    def wrapped(*args, **kwargs):
        request = args[0]
        if 'logged_user' not in request.session:
            raise UserNotLogged('Usuário não logado ou sessão vencida')

        if sessionService.logged_user(request)['role'] != 1:
            raise UserNotLogged('Usuário não é admin')

        return f(*args, **kwargs)

    return wrapped

