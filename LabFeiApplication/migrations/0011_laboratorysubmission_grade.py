# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LabFeiApplication', '0010_auto_20140813_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratorysubmission',
            name='grade',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
