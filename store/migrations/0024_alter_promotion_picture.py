# Generated by Django 3.2.5 on 2022-01-13 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_category_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='picture',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]