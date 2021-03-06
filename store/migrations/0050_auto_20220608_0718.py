# Generated by Django 3.2.7 on 2022-06-08 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0049_auto_20220607_0443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказы', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='client',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_client', to='store.order'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_percent',
            field=models.IntegerField(blank=True, null=True, verbose_name='скидка'),
        ),
    ]
