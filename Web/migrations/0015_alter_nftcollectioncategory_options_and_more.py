# Generated by Django 4.0.3 on 2022-04-19 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0014_nftcollection_category_nftcollection_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nftcollectioncategory',
            options={'verbose_name_plural': 'NFT Collection Categories'},
        ),
        migrations.AlterField(
            model_name='nftcollection',
            name='category',
            field=models.ForeignKey(null=True, on_delete=models.SET('user_deleted'), related_name='category', to='Web.nftcollectioncategory', verbose_name='Category of the NFT Collection.'),
        ),
        migrations.AlterField(
            model_name='nftcollection',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description of the NFT given by the creator.'),
        ),
    ]
