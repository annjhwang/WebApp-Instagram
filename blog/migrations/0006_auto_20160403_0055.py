# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-03 00:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20160402_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='image',
            new_name='image_url',
        ),
        migrations.AddField(
            model_name='image',
            name='Posts',
            field=models.IntegerField(null=True),
        ),
    ]
