# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0025_remove_jsscomputerattributemapping_jsssite'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsscomputerattributemapping',
            name='jsssite',
            field=models.ForeignKey(default=1, to='jssmanifests.JSSSite'),
        ),
    ]
