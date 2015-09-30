# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0004_auto_20150515_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsscomputerattributemapping',
            name='manifest_element_type',
            field=models.CharField(max_length=b'1', verbose_name=b'Manifest Element', choices=[(b'c', b'Catalog'), (b'm', b'Manifest'), (b'p', b'Package')]),
        ),
        migrations.AlterField(
            model_name='jsscomputerattributemapping',
            name='package_action',
            field=models.IntegerField(blank=True, verbose_name=b'Package Action', choices=[(b'managed_installs', b'Managed installs'), (b'managed_uninstalls', b'Managed uninstalls'), (b'managed_updates', b'Managed updates'), (b'optional_installs', b'Optional installs')]),
        ),
    ]
