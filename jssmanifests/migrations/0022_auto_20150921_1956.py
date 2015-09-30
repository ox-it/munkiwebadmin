# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0021_auto_20150921_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jsscomputerattributemapping',
            name='site',
        ),
        migrations.AlterField(
            model_name='jssuser',
            name='sites',
            field=models.ManyToManyField(to='jssmanifests.JSSSite', blank=True),
        ),
    ]
