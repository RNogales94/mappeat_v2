# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 18:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainRest', '0028_auto_20170709_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='province',
            field=models.CharField(blank=True, max_length=90),
        ),
        migrations.AlterField(
            model_name='ticket_detail',
            name='time_of_meal',
            field=models.TimeField(default=datetime.time(18, 4, 6, 536450)),
        ),
        migrations.AlterField(
            model_name='ticket_resume',
            name='date_of_meal',
            field=models.DateField(db_index=True, default=datetime.datetime(2017, 7, 10, 18, 4, 6, 535727, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ticket_resume',
            name='time_of_meal',
            field=models.TimeField(db_index=True, default=datetime.time(18, 4, 6, 535759)),
        ),
    ]