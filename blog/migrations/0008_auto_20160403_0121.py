# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-03 01:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_image_image_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='Followers',
            field=models.IntegerField(null=True),
        ),
    ]