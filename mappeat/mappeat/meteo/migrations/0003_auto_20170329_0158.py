# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 23:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meteo', '0002_auto_20170328_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='direction',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='hora_pres_max',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='hora_pres_min',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='hora_racha',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='hora_tmax',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='hora_tmin',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='prec',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='pres_max',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='pres_min',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='racha',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='sol',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='tmax',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='tmed',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='tmin',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='vel_media',
            field=models.FloatField(null=True),
        ),
    ]
