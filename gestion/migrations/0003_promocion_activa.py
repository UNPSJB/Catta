# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-11 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_auto_20171203_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocion',
            name='activa',
            field=models.BooleanField(default=True),
        ),
    ]
