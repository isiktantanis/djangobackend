# Generated by Django 4.0.3 on 2022-04-07 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0005_alter_user_profilepicture'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nft',
            options={'verbose_name': 'NFT'},
        ),
        migrations.RemoveField(
            model_name='nft',
            name='parent',
        ),
    ]
