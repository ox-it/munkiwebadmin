# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsscomputerattributetype',
            name='api_endpoint',
            field=models.CharField(max_length=1024, verbose_name=b'API Endpoint (data retrival)', blank=True),
        ),
        migrations.AlterField(
            model_name='jsscomputerattributetype',
            name='label',
            field=models.CharField(max_length=1024, verbose_name=b'Type Label'),
        ),
        migrations.AlterField(
            model_name='jsscomputerattributetype',
            name='xpath',
            field=models.CharField(max_length=1024, verbose_name=b'XPath for extraction', blank=True),
        ),
    ]
