# Generated by Django 5.0 on 2024-02-04 21:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FridgeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('quantity', models.IntegerField(default=0)),
                ('min_reminder', models.IntegerField()),
                ('expiry_date', models.DateTimeField(null=True)),
                ('last_added', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'FridgeItem',
                'verbose_name_plural': 'FridgeItems',
            },
        ),
        migrations.CreateModel(
            name='Suplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=16, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FridgeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(choices=[(1, 'Added'), (2, 'Removed')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fridge.fridgeitem')),
            ],
        ),
        migrations.AddField(
            model_name='fridgeitem',
            name='suplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fridge.suplier'),
        ),
    ]
