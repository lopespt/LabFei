# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LabFeiApplication', '0005_laboratorysubmission_laboratory'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorrectionErrors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=12)),
                ('description', models.TextField()),
                ('laboratorySubmission', models.ForeignKey(to='LabFeiApplication.LaboratorySubmission')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
