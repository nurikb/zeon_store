# Generated by Django 3.2.7 on 2022-05-27 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_remove_helpimage_help_obj'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='help',
            options={'verbose_name': 'Вопросы и ответы', 'verbose_name_plural': 'Вопросы и ответы'},
        ),
        migrations.AlterModelOptions(
            name='helpimage',
            options={'verbose_name': 'Картинка для страницы "Помощь"', 'verbose_name_plural': 'Картинка для страницы "Помощь"'},
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]