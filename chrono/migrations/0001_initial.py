# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-29 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('start_dt', models.DateTimeField()),
                ('end_dt', models.DateTimeField()),
                ('venue', models.CharField(max_length=200)),
                ('organizer_name', models.CharField(max_length=200)),
                ('organizer_contact', models.CharField(max_length=200)),
                ('organizer_mail', models.CharField(max_length=200)),
            ],
        ),
    ]
