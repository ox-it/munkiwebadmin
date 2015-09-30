# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0018_auto_20150618_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsscomputerattributemapping',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name=b'Mapping enabled'),
        ),
    ]
