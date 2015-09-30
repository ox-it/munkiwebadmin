# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0017_remove_jsscomputerattributetype__provided_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsscomputerattributemapping',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name=b'Is this mapping enabled'),
        ),
        migrations.AlterField(
            model_name='jsscomputerattributetype',
            name='xpath_needs_key',
            field=models.BooleanField(default=False, verbose_name=b'Key required for data extraction from xpath'),
        ),
    ]
