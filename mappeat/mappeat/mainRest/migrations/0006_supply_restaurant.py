# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-14 09:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainRest', '0005_ticket_resume_cost_without_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='supply',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainRest.Restaurant'),
        ),
    ]
