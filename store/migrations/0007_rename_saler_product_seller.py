# Generated by Django 3.2.5 on 2021-12-12 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_saler'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='saler',
            new_name='seller',
        ),
    ]
