# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-07 18:04


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locking', '0002_auto_20150706_1054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lock',
            options={'ordering': ('-_locked_at',), 'permissions': (('unlocker', 'Can break record locks.'),)},
        ),
    ]
