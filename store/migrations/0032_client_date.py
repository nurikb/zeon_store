# Generated by Django 3.2.7 on 2022-06-02 06:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_auto_20220602_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]