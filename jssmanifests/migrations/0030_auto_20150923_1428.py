# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('jssmanifests', '0029_jsssite_businessunit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jsssite',
            options={'permissions': (('can_view_jsssite', 'Can view JSS Site'), ('can_edit_jsssite', 'Can edit JSS Site'))},
        ),
        migrations.AddField(
            model_name='jsssite',
            name='group',
            field=models.OneToOneField(default='-1', to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jsssite',
            name='businessunit',
            field=models.ForeignKey(default=None, blank=True, to='reports.BusinessUnit', null=True),
        ),
    ]
