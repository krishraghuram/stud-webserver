# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-30 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chrono', '0002_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='sent_from',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='email',
            name='sent_to',
            field=models.CharField(max_length=1000),
        ),
    ]