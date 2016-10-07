# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-07 18:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='Duenia',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='personas.Duenia'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='cliente',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='personas.Cliente'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='empleado',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='personas.Empleado'),
        ),
    ]
