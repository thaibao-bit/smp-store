# Generated by Django 3.2.5 on 2022-01-13 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_alter_promotion_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='picture',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]