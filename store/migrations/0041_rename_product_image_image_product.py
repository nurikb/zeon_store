# Generated by Django 3.2.7 on 2022-06-02 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0040_alter_image_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='product_image',
            new_name='product',
        ),
    ]
