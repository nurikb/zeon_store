# Generated by Django 3.2.7 on 2022-06-02 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0041_rename_product_image_image_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=12, max_digits=12),
        ),
    ]
