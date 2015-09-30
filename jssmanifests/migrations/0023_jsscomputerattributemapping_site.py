# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0022_auto_20150921_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsscomputerattributemapping',
            name='site',
            field=models.CharField(max_length=1024, verbose_name=b'Site', blank=True),
        ),
    ]
