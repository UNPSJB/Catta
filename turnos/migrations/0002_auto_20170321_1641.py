# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-21 16:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='dia',
            field=models.DateField(default=datetime.date(2017, 3, 21)),
        ),
        migrations.AddField(
            model_name='turno',
            name='hora',
            field=models.TimeField(default='16:41:02'),
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_creacion',
            field=models.DateField(default=datetime.date(2017, 3, 21), null=True),
        ),
    ]
