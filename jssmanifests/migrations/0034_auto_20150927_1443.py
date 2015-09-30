# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0033_auto_20150925_1314'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jsscomputerattributemapping',
            options={'verbose_name': 'JSS Computer Attribute Mapping', 'verbose_name_plural': 'JSS Computer Attribute Mappings', 'permissions': (('can_view_jsscomputerattributemapping', 'Can view JSS Computer Attribute Mappings'),)},
        ),
        migrations.AlterModelOptions(
            name='jsscomputerattributetype',
            options={'verbose_name': 'JSS Computer Attribute Type', 'verbose_name_plural': 'JSS Computer Attribute Types'},
        ),
        migrations.AlterModelOptions(
            name='jssuser',
            options={'verbose_name': 'JSS User', 'verbose_name_plural': 'JSS Users'},
        ),
    ]
