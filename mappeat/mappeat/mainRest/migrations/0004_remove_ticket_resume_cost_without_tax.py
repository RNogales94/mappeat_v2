# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-08 16:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainRest', '0003_auto_20170908_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket_resume',
            name='cost_without_tax',
        ),
    ]
