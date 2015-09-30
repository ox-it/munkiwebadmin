# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0012_jsscomputerattributetype_xpath_needs_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jsscomputerattributetype',
            old_name='xpath_expression',
            new_name='computer_xpath',
        ),
        migrations.RemoveField(
            model_name='jsscomputerattributetype',
            name='api_endpoint',
        ),
        migrations.AddField(
            model_name='jsscomputerattributetype',
            name='api_path',
            field=models.CharField(max_length=1024, verbose_name=b'API URI (api path to this object)', blank=True),
        ),
        migrations.AddField(
            model_name='jsscomputerattributetype',
            name='api_xpath',
            field=models.CharField(max_length=1024, verbose_name=b'API Xpath (expression to extract data from the API object)', blank=True),
        ),
        migrations.AlterField(
            model_name='jsscomputerattributetype',
            name='xpath_needs_key',
            field=models.BooleanField(default=False, verbose_name=b'Key required for data extraction'),
        ),
    ]
