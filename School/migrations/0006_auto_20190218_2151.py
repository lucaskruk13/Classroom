# Generated by Django 2.1.5 on 2019-02-18 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('School', '0005_remove_session_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='absences',
            field=models.ManyToManyField(blank=True, null=True, to='Account.Profile'),
        ),
    ]
