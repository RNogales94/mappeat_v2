# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 16:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainRest', '0036_auto_20170718_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='date',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ticket_detail',
            name='time_of_meal',
            field=models.TimeField(default=datetime.time(16, 54, 41, 110376)),
        ),
        migrations.AlterField(
            model_name='ticket_resume',
            name='date_of_meal',
            field=models.DateField(db_index=True, default=datetime.datetime(2017, 7, 18, 16, 54, 41, 109638, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ticket_resume',
            name='time_of_meal',
            field=models.TimeField(db_index=True, default=datetime.time(16, 54, 41, 109669)),
        ),
    ]
