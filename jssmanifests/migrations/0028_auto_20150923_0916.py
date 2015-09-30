# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0027_jsssite_last_refresh'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jsssite',
            options={'permissions': (('can_view_jsssite', 'Can view JSS Site'),)},
        ),
    ]
