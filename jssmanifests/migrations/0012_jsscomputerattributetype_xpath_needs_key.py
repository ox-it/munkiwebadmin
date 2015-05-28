# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0011_auto_20150527_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsscomputerattributetype',
            name='xpath_needs_key',
            field=models.BooleanField(default=False, verbose_name=b'Key required for expression'),
        ),
    ]
