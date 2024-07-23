# Generated by Django 4.2.10 on 2024-07-23 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0005_property_primary_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='primary_photo',
            field=models.ImageField(blank=True, null=True, upload_to='property_photos/'),
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]