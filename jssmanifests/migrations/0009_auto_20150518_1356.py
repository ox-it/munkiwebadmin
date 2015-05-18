# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0008_auto_20150518_0855'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jsscomputerattributemapping',
            old_name='priority',
            new_name='priorty',
        ),
    ]
