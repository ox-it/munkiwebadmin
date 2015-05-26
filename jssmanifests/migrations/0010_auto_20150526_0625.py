# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0009_auto_20150518_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jsscomputerattributetype',
            name='jss_field',
        ),
        migrations.AddField(
            model_name='jsscomputerattributetype',
            name='xpath_expression',
            field=models.CharField(max_length=1024, verbose_name=b'XPath expression', blank=True),
        ),
    ]
