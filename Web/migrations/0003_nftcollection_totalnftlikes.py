# Generated by Django 4.0.3 on 2022-06-16 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Web", "0002_alter_nftcollection_owner_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="nftcollection",
            name="totalNFTLikes",
            field=models.IntegerField(
                default=0,
                verbose_name="Total Number of Likes of all NFT's inside the Collection",
            ),
        ),
    ]
