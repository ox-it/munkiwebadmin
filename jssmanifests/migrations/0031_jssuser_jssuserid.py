# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0030_auto_20150923_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='jssuser',
            name='jssuserid',
            field=models.IntegerField(default=1, verbose_name=b'JSS User ID'),
            preserve_default=False,
        ),
    ]
