# Generated by Django 4.1 on 2022-08-08 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_listing_image_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_upload',
            field=models.ImageField(blank=True, null=True, upload_to='staticfiles/auctions/images'),
        ),
    ]
