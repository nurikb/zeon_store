# Generated by Django 3.2.7 on 2022-05-31 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_help_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='help',
            name='image',
        ),
    ]
