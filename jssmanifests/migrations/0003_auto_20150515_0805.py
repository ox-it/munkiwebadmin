# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jssmanifests', '0002_auto_20150511_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='JSSComputerAttributeMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jss_computer_attribute_key', models.CharField(max_length=1024, verbose_name=b'Attribute Key')),
                ('jss_computer_attribute_value', models.CharField(max_length=1024, verbose_name=b'Attribute Value')),
                ('manifest_element_type', models.CharField(max_length=b'1', verbose_name=b'Manifest Element', choices=[(b'c', b'Catalog'), (b'm', b'manifest'), (b'p', b'Package')])),
                ('catalog_name', models.CharField(max_length=1024, verbose_name=b'Catalog Name', blank=True)),
                ('package_name', models.CharField(max_length=1024, verbose_name=b'Package Name', blank=True)),
                ('package_action', models.IntegerField(blank=True, verbose_name=b'Package Action', choices=[(b'Managed installs', b'managed_installs'), (b'Managed uninstalls', b'managed_uninstalls'), (b'Managed updates', b'managed_updates'), (b'Optional installs', b'optional_installs')])),
                ('manifest_name', models.CharField(max_length=1024, verbose_name=b'Manifest Name', blank=True)),
                ('remove_from_xml', models.BooleanField(verbose_name=b'Remove from Manifest')),
                ('priorty', models.IntegerField(verbose_name=b'Priorty')),
                ('site', models.CharField(max_length=1024, verbose_name=b'Manifest Name', blank=True)),
            ],
            options={
                'verbose_name': 'Computer Attribute Mapping',
                'verbose_name_plural': 'Computer Attribute Mappings',
            },
        ),
        migrations.AlterModelOptions(
            name='jsscomputerattributetype',
            options={'verbose_name': 'Computer Attribute Type', 'verbose_name_plural': 'Computer Attribute Types'},
        ),
        migrations.AddField(
            model_name='jsscomputerattributemapping',
            name='jss_computer_attribute_type',
            field=models.ForeignKey(to='jssmanifests.JSSComputerAttributeType'),
        ),
    ]
