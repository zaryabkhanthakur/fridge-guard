# Generated by Django 5.0 on 2024-02-05 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fridge', '0002_alter_fridgehistory_action'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fridgeitem',
            name='suplier',
        ),
        migrations.AddField(
            model_name='fridgeitem',
            name='auto_order',
            field=models.BooleanField(default=True),
        ),
    ]
