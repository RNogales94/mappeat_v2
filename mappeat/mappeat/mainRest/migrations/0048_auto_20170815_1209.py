# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-15 10:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainRest', '0047_auto_20170814_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='date',
            field=models.DateField(db_index=True, default=datetime.date(2017, 8, 15)),
        ),
        migrations.AlterField(
            model_name='ticket_detail',
            name='time',
            field=models.TimeField(default=datetime.time(10, 9, 17, 288094)),
        ),
        migrations.AlterField(
            model_name='ticket_resume',
            name='date',
            field=models.DateField(db_index=True, default=datetime.date(2017, 8, 15)),
        ),
        migrations.AlterField(
            model_name='ticket_resume',
            name='time',
            field=models.TimeField(db_index=True, default=datetime.time(10, 9, 17, 287385)),
        ),
    ]