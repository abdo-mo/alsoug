# Generated by Django 4.1 on 2022-08-09 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_remove_listing_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='image_upload',
            new_name='image',
        ),
    ]