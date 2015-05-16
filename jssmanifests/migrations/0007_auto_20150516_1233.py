# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0006_auto_20150515_0820'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jsscomputerattributetype',
            name='xpath',
        ),
        migrations.AddField(
            model_name='jsscomputerattributetype',
            name='jss_field',
            field=models.CharField(max_length=1024, verbose_name=b'JSS Field name', blank=True),
        ),
    ]
