# Generated by Django 4.1 on 2022-09-10 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_listing_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='catagory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
