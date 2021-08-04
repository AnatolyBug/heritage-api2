# Generated by Django 3.2.5 on 2021-08-03 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='saved_places',
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(blank=True, default='default_avatar.png'),
        ),
    ]
