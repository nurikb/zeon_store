# Generated by Django 3.2.7 on 2022-06-02 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_auto_20220602_0745'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='discount',
            new_name='discount_sum',
        ),
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
    ]
