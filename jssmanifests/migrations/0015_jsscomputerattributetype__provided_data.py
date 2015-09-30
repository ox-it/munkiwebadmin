# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0014_auto_20150528_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsscomputerattributetype',
            name='_provided_data',
            field=models.BooleanField(default=False, verbose_name=b'data provided with application'),
        ),
    ]
