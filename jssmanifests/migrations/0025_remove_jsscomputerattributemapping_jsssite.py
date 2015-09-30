# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0024_jsscomputerattributemapping_jsssite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jsscomputerattributemapping',
            name='jsssite',
        ),
    ]
