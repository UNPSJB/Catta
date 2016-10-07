# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-06 22:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='insumo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('contenidoNeto', models.IntegerField(default=0)),
                ('marca', models.CharField(max_length=100)),
                ('stock', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('nombre', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('nombre', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
                ('precio', models.IntegerField(default=0)),
                ('duracion', models.IntegerField(default=0)),
            ],
        ),
    ]
