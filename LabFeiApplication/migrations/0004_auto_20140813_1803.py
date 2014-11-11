# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LabFeiApplication', '0003_course_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratorysubmission',
            name='status',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='laboratorysubmission',
            name='zippedFile',
            field=models.FilePathField(default=''),
            preserve_default=False,
        ),
    ]
