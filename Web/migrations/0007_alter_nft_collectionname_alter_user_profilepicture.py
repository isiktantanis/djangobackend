# Generated by Django 4.0.4 on 2022-05-02 20:17

import Web.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0006_alter_nft_metadatatype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nft',
            name='collectionName',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Web.nftcollection', verbose_name='Collection Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profilePicture',
            field=models.ImageField(blank=True, null=True, storage=Web.models.OverwriteStorage(), upload_to=Web.models.FileUploadLocation(fields=['username'], parentFolder='profilePictures/'), verbose_name='Profile Picture'),
        ),
    ]
