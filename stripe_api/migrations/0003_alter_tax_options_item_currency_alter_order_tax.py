# Generated by Django 4.1.6 on 2023-02-12 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_api', '0002_alter_tax_options_order_tax_tax_tax_size_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name': 'Налог', 'verbose_name_plural': 'Проценты налога'},
        ),
        migrations.AddField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('rub', 'Рубль'), ('usd', 'Доллар')], default='rub', max_length=3, verbose_name='Тип валюты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='tax',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='stripe_api.tax', verbose_name='Процент налога'),
        ),
    ]
