# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LabFeiApplication', '0006_correctionerrors'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorrectionConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('replaceMain', models.BooleanField()),
                ('mainReplacement', models.TextField()),
                ('inputStream', models.TextField()),
                ('laboratory', models.ForeignKey(to='LabFeiApplication.Laboratory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
