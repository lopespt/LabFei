# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LabFeiApplication', '0009_auto_20140813_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratorysubmission',
            name='status',
            field=models.CharField(max_length=15),
        ),
    ]
