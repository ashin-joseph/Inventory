# Generated by Django 5.0.6 on 2024-08-29 07:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='rsit_backup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rsit_b_item', models.CharField(blank=True, max_length=100, null=True)),
                ('rsit_b_reason', models.CharField(blank=True, max_length=100, null=True)),
                ('rsit_b_qty', models.PositiveIntegerField(blank=True, null=True)),
                ('rsit_b_price', models.CharField(blank=True, max_length=100, null=True)),
                ('rsit_b_tax', models.CharField(blank=True, max_length=100, null=True)),
                ('rsit_b_offer', models.CharField(blank=True, max_length=100, null=True)),
                ('rsit_b_refundAmount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='rst_backup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rst_b_billNum', models.CharField(max_length=50, unique=True)),
                ('rst_b_poNum', models.CharField(blank=True, max_length=100, null=True)),
                ('rst_b_date', models.CharField(blank=True, max_length=100, null=True)),
                ('rst_b_user', models.CharField(blank=True, max_length=100, null=True)),
                ('sot_b_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='salesorderItemTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soit_quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('soit_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='salesorderTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sot_bill_number', models.CharField(max_length=50, unique=True)),
                ('sot_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='soit_backup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soit_b_item', models.CharField(blank=True, max_length=100, null=True)),
                ('soit_b_quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('soit_b_price', models.CharField(blank=True, max_length=100, null=True)),
                ('soit_b_tax', models.CharField(blank=True, max_length=100, null=True)),
                ('soit_b_offer', models.CharField(blank=True, max_length=100, null=True)),
                ('soit_b_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='sot_backup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sot_b_bill_number', models.CharField(max_length=50, unique=True)),
                ('sot_b_date', models.CharField(blank=True, max_length=100, null=True)),
                ('sot_b_user', models.CharField(blank=True, max_length=100, null=True)),
                ('sot_b_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='returnsalesItemTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rsit_reason', models.CharField(blank=True, max_length=100, null=True)),
                ('rsit_qty', models.PositiveIntegerField(blank=True, null=True)),
                ('rsit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('rsit_tax', models.PositiveIntegerField(blank=True, null=True)),
                ('rsit_offer', models.PositiveIntegerField(blank=True, null=True)),
                ('rsit_refundAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rsit_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.itemtable')),
            ],
        ),
        migrations.CreateModel(
            name='returnSalesTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rst_billNum', models.CharField(max_length=50, unique=True)),
                ('rst_poNum', models.CharField(max_length=50)),
                ('rst_date', models.DateField(auto_now_add=True)),
                ('rst_item', models.ManyToManyField(through='Sales.returnsalesItemTable', to='Core.itemtable')),
            ],
        ),
    ]
