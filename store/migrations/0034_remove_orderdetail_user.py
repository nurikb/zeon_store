# Generated by Django 3.2.7 on 2022-06-02 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_client_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='user',
        ),
    ]
