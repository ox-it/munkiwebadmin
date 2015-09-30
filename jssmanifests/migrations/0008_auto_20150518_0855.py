# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0007_auto_20150516_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsscomputerattributemapping',
            name='priority',
            field=models.IntegerField(default=0, verbose_name=b'Priorty'),
        ),
    ]
