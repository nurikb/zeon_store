# Generated by Django 3.2.7 on 2022-05-31 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_auto_20220531_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='advantage',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
