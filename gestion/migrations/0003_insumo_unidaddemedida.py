# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-19 23:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_auto_20161119_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='insumo',
            name='unidadDeMedida',
            field=models.CharField(choices=[(1, 'Minilitros'), (2, 'Litros'), (3, 'Gramos'), (4, 'Kilos'), (0, 'Centimetros Cubicos')], default=0, max_length=1),
        ),
    ]
