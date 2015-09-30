# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0023_jsscomputerattributemapping_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsscomputerattributemapping',
            name='jsssite',
            field=models.ForeignKey(default=17, blank=True, to='jssmanifests.JSSSite'),
            preserve_default=False,
        ),
    ]
