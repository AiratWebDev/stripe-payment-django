# Generated by Django 4.1.6 on 2023-02-13 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_api', '0007_alter_item_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена'),
        ),
    ]