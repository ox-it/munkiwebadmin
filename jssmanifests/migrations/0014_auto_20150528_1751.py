# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0013_auto_20150528_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsscomputerattributetype',
            name='computer_xpath',
            field=models.CharField(max_length=1024, verbose_name=b'XPath expression'),
        ),
    ]
