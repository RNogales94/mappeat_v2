# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-19 09:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainRest', '0038_auto_20170718_1858'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='avalible',
            new_name='available',
        ),
        migrations.AlterField(
            model_name='inventory',
            name='date',
            field=models.DateField(db_index=True, default=datetime.date(2017, 7, 19)),
        ),
        migrations.AlterField(
            model_name='ticket_detail',
            name='time_of_meal',
            field=models.TimeField(default=datetime.time(9, 43, 10, 291112)),
        ),
        migrations.AlterField(
            model_name='ticket_resume',
            name='date_of_meal',
            field=models.DateField(db_index=True, default=datetime.datetime(2017, 7, 19, 9, 43, 10, 290236, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ticket_resume',
            name='time_of_meal',
            field=models.TimeField(db_index=True, default=datetime.time(9, 43, 10, 290266)),
        ),
    ]
