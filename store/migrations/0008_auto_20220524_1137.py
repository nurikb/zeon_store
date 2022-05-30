# Generated by Django 3.2.7 on 2022-05-24 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20220524_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='color',
            field=models.CharField(max_length=255, null=True, verbose_name='цвет'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
