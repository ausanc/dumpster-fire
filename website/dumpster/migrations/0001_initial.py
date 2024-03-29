# Generated by Django 2.0.4 on 2018-12-01 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_url', models.URLField(default=None)),
                ('game_id', models.CharField(default=None, max_length=255)),
                ('achievement_id', models.CharField(default=None, max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('completed_on', models.DateTimeField(blank=True, default=None, editable=False, null=True)),
            ],
        ),
    ]
