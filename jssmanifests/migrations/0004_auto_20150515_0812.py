# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0003_auto_20150515_0805'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jsscomputerattributemapping',
            old_name='priorty',
            new_name='priority',
        ),
        migrations.AlterField(
            model_name='jsscomputerattributemapping',
            name='site',
            field=models.CharField(max_length=1024, verbose_name=b'Site', blank=True),
        ),
    ]
