# Generated by Django 4.0.3 on 2022-04-19 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0009_user_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='slug',
        ),
    ]