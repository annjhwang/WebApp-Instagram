# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-11 23:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_image_post_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='Followers',
        ),
        migrations.RemoveField(
            model_name='image',
            name='Following',
        ),
        migrations.RemoveField(
            model_name='image',
            name='Posts',
        ),
    ]
