# Generated by Django 3.2.7 on 2022-05-31 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_remove_help_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='help',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store.helpimage'),
        ),
    ]
