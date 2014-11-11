# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('insertionDate', models.DateTimeField()),
                ('openDate', models.DateTimeField()),
                ('closeDate', models.DateTimeField()),
                ('course', models.ForeignKey(to='LabFeiApplication.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LaboratoryFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30, null=True)),
                ('file', models.FilePathField()),
                ('laboratory', models.ForeignKey(to='LabFeiApplication.Laboratory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LaboratorySubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateSubmitted', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubmittedFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FilePathField()),
                ('laboratorySubmission', models.ForeignKey(to='LabFeiApplication.LaboratorySubmission')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('login', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='laboratorysubmission',
            name='user',
            field=models.ForeignKey(to='LabFeiApplication.User'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='UserCourses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subscriptionDate', models.DateTimeField()),
                ('course', models.ForeignKey(to='LabFeiApplication.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(to='LabFeiApplication.Course', through='LabFeiApplication.UserCourses'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercourses',
            name='user',
            field=models.ForeignKey(to='LabFeiApplication.User'),
            preserve_default=True,
        ),
    ]
