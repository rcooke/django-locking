# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('locking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lock',
            name='_locked_by',
            field=models.ForeignKey(related_name='working_on_locking_lock', on_delete=models.CASCADE, db_column='locked_by', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
