# Generated by Django 2.1.3 on 2018-12-01 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dumpster', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hook',
            name='ach_name',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='hook',
            name='game_name',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='hook',
            name='icon_url',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
