# Generated by Django 3.2.7 on 2022-06-02 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0039_rename_product_image_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='product_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='store.product'),
        ),
    ]
