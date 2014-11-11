# -*- coding: utf-8 -*-
from LabFeiApplication.services import sessionService

__author__ = 'wachs'
from django.template import RequestContext


def base_url(request):
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'


    return {'BASE_URL': scheme + request.get_host()}


def logged_user_info(request):
    user = sessionService.logged_user(request)
    return {'logged_user': user}
