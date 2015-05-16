# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0005_auto_20150515_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsscomputerattributemapping',
            name='package_action',
            field=models.CharField(blank=True, max_length=256, verbose_name=b'Package Action', choices=[(b'managed_installs', b'Managed installs'), (b'managed_uninstalls', b'Managed uninstalls'), (b'managed_updates', b'Managed updates'), (b'optional_installs', b'Optional installs')]),
        ),
    ]
