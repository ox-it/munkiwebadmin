# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0032_auto_20150925_0819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jsscomputerattributemapping',
            name='site',
        ),
        migrations.AddField(
            model_name='jsscomputerattributetype',
            name='computer_xpath',
            field=models.CharField(default=1, max_length=1024, verbose_name=b'XPath expression'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jsscomputerattributemapping',
            name='jss_computer_attribute_type',
            field=models.ForeignKey(verbose_name=b'Computer Attribute Type', to='jssmanifests.JSSComputerAttributeType'),
        ),
        migrations.AlterField(
            model_name='jsscomputerattributemapping',
            name='jsssite',
            field=models.ForeignKey(verbose_name=b'JSS Site', to='jssmanifests.JSSSite'),
        ),
        migrations.AlterField(
            model_name='jsssite',
            name='businessunit',
            field=models.ForeignKey(default=None, blank=True, to='reports.BusinessUnit', null=True, verbose_name=b'Business Unit'),
        ),
        migrations.AlterField(
            model_name='jsssite',
            name='group',
            field=models.OneToOneField(verbose_name=b'Related Group', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='jssuser',
            name='sites',
            field=models.ManyToManyField(to='jssmanifests.JSSSite', verbose_name=b'JSS Site(s)', blank=True),
        ),
    ]
