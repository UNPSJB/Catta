# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-19 23:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviciobasico',
            name='insumos',
            field=models.ManyToManyField(blank=True, to='gestion.Insumo'),
        ),
    ]