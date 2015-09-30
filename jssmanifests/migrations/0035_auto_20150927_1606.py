# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0034_auto_20150927_1443'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jsscomputerattributemapping',
            old_name='priorty',
            new_name='priority',
        ),
    ]
