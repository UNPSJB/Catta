# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-25 17:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0002_auto_20170325_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='dia',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_creacion',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='turno',
            name='hora',
            field=models.TimeField(default=datetime.time(17, 15, 55, 405849)),
        ),
    ]
