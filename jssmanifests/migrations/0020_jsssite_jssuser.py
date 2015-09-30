# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jssmanifests', '0019_auto_20150618_1543'),
    ]

    operations = [
        migrations.CreateModel(
            name='JSSSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jsssiteid', models.IntegerField(verbose_name=b'JSS Site ID')),
                ('jsssitename', models.CharField(max_length=1024, verbose_name=b'Type Label')),
            ],
        ),
        migrations.CreateModel(
            name='JSSUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lastrefresh', models.DateTimeField(auto_now=True)),
                ('sites', models.ManyToManyField(to='jssmanifests.JSSSite')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
