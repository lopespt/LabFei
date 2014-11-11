# -*- coding: utf-8 -*-
from LabFeiApplication.management.commands.entities.entity import Entity

__author__ = 'wachs'

from django.core.management import BaseCommand
from LabFeiApplication.models import *
from django.utils import timezone

curso = [Course(name='curso1', description="Minha descrição"),
         Course(name='curso2', description="Minha descrição 2")]

usuario = [User(name='Guilherme2', login='lopespt', password='teste', email='guilhermewachs@gmail.com', role=0),
           User(name='Joãozinho', login='teste', password='teste', email='joãozinho@gmail.com', role=1)]

usuario_curso = [UserCourses(user=usuario[0], course=curso[0], subscriptionDate=timezone.now()),
                 UserCourses(user=usuario[0], course=curso[1], subscriptionDate=timezone.now())]

laboratory = [
    Laboratory(course=curso[0], title='Lab 1 curso 1', description='Descrição lab 1 curso 1', insertionDate=timezone.now(), openDate=timezone.now(), closeDate=timezone.now() ),
    Laboratory(course=curso[0], title='Lab 2 curso 1', description='Descrição lab 2 curso 1', insertionDate=timezone.now(), openDate=timezone.now(), closeDate=timezone.now() ),
    Laboratory(course=curso[1], title='Lab 1 curso 2', description='Descrição lab 1 curso 2', insertionDate=timezone.now(), openDate=timezone.now(), closeDate=timezone.now() )
]

laboratoryFiles = [
    LaboratoryFile(laboratory=laboratory[0], title='Arquivo1', file='/Users/wachs/sqldump.sql')
]

class Command(BaseCommand):
    help = "Insere dados iniciais no banco"

    def execute(self, *args, **options):
        Entity(User, usuario, 'name')
        Entity(Course, curso, 'name')
        Entity(UserCourses, usuario_curso, ['user__name', 'course__name'])
        Entity(Laboratory, laboratory, ['course__name', 'title'])
        Entity(LaboratoryFile, laboratoryFiles, ['laboratory__title', 'title'])


