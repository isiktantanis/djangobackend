# Generated by Django 4.0.4 on 2022-07-15 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0002_rename_address_nft_collection_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nft',
            name='collection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='Web.nftcollection', verbose_name='Collection'),
        ),
    ]