# Generated by Django 4.2.9 on 2024-02-06 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fridge', '0005_fridgeitem_default_order_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fridgeitem',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
    ]
