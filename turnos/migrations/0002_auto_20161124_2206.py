# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='promociones',
            field=models.ManyToManyField(blank=True, related_name='turnos', to='gestion.Promocion'),
        ),
        migrations.AlterField(
            model_name='turno',
            name='servicios',
            field=models.ManyToManyField(blank=True, related_name='turnos', to='gestion.ServicioBasico'),
        ),
    ]
