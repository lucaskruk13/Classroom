# Generated by Django 2.1.5 on 2019-02-18 21:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('School', '0002_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 18, 21, 49, 34, 462290, tzinfo=utc), null=True),
        ),
    ]
