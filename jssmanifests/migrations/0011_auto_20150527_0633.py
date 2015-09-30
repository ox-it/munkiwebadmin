# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0010_auto_20150526_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsscomputerattributemapping',
            name='jss_computer_attribute_key',
            field=models.CharField(max_length=1024, verbose_name=b'Attribute Key', blank=True),
        ),
    ]
