# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '__first__'),
        ('jssmanifests', '0028_auto_20150923_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsssite',
            name='businessunit',
            field=models.OneToOneField(default='THIS SHOULD NEVER BE USED', to='reports.BusinessUnit'),
            preserve_default=False,
        ),
    ]
