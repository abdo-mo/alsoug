# Generated by Django 4.0.3 on 2022-08-23 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_rename_image_upload_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
