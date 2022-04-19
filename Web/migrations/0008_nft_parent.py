# Generated by Django 4.0.3 on 2022-04-07 17:57

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0007_alter_nft_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='nft',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='Web.nft'),
        ),
    ]
