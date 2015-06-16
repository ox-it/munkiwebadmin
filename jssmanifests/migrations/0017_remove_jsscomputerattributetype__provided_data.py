# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0016_auto_20150615_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jsscomputerattributetype',
            name='_provided_data',
        ),
    ]
