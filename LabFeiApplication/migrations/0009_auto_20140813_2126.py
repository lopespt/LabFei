# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LabFeiApplication', '0008_correctionconfiguration_expectedoutput'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='correctionconfiguration',
            name='laboratory',
        ),
        migrations.DeleteModel(
            name='CorrectionConfiguration',
        ),
        migrations.AddField(
            model_name='laboratory',
            name='expectedOutput',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='laboratory',
            name='inputStream',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='laboratory',
            name='mainReplacement',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='laboratory',
            name='replaceMain',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
