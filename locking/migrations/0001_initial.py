# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', to_field='id', on_delete=models.CASCADE)),
                ('object_id', models.PositiveIntegerField()),
                ('_locked_at', models.DateTimeField(null=True, editable=False, db_column='locked_at')),
                ('_locked_by', models.ForeignKey(db_column='locked_by', to_field='id', editable=False, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
                ('_hard_lock', models.BooleanField(default=False, editable=False, db_column='hard_lock')),
            ],
            options={
                'ordering': ('-_locked_at',),
            },
            bases=(models.Model,),
        ),
    ]
