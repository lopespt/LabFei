# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LabFeiApplication', '0007_correctionconfiguration'),
    ]

    operations = [
        migrations.AddField(
            model_name='correctionconfiguration',
            name='expectedOutput',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
