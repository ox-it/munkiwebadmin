# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0020_jsssite_jssuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jssuser',
            old_name='lastrefresh',
            new_name='last_site_refresh',
        ),
    ]
