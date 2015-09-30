# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0026_jsscomputerattributemapping_jsssite'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsssite',
            name='last_refresh',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 18, 0, 11, 764967), auto_now=True),
            preserve_default=False,
        ),
    ]
