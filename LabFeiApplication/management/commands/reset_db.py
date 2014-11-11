# -*- coding: utf-8 -*-
from LabFeiApplication.management.commands.entities.entity import Entity

__author__ = 'wachs'

from django.core.management import BaseCommand
from LabFeiApplication.models import *


class Command(BaseCommand):
    help = "Deleta dados do banco"

    def execute(self, *args, **options):
        Laboratory.objects.all().delete()
        UserCourses.objects.all().delete()
        User.objects.all().delete()
        Course.objects.all().delete()


