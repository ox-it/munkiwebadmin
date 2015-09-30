# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0031_jssuser_jssuserid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jsssite',
            options={'verbose_name': 'JSS Site', 'verbose_name_plural': 'JSS Sites', 'permissions': (('can_view_jsssite', 'Can view JSS Site'), ('can_edit_jsssite', 'Can edit JSS Site'))},
        ),
        migrations.RemoveField(
            model_name='jsscomputerattributetype',
            name='computer_xpath',
        ),
        migrations.AlterField(
            model_name='jsscomputerattributemapping',
            name='jsssite',
            field=models.ForeignKey(to='jssmanifests.JSSSite'),
        ),
    ]
