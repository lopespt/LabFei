# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LabFeiApplication', '0004_auto_20140813_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratorysubmission',
            name='laboratory',
            field=models.ForeignKey(default=1, to='LabFeiApplication.Laboratory'),
            preserve_default=False,
        ),
    ]
