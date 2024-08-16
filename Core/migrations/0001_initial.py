# Generated by Django 5.0.6 on 2024-08-16 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='itemTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('item_category', models.CharField(choices=[('Vegetables', 'Veg'), ('Fruits', 'Fru')], max_length=50)),
                ('item_unit', models.CharField(choices=[('Kilogram', 'Kg'), ('Pieces', 'Pcs')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='vendorTable',
            fields=[
                ('vendor_id', models.AutoField(primary_key=True, serialize=False)),
                ('vendor_shop_name', models.CharField(blank=True, max_length=100, null=True)),
                ('vendor_location', models.CharField(blank=True, max_length=50, null=True)),
                ('vendor_pin', models.CharField(blank=True, max_length=6, null=True)),
                ('vendor_email', models.EmailField(blank=True, max_length=100, null=True)),
                ('vendor_name', models.CharField(blank=True, max_length=50, null=True)),
                ('vendor_phone', models.CharField(blank=True, max_length=10, null=True)),
                ('vendor_GST', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('vendor_note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='priceTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pt_sellingPrice', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('pt_tax', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('pt_offer', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('pt_timestamp', models.DateTimeField(auto_now_add=True)),
                ('pt_item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Core.itemtable')),
            ],
        ),
    ]
