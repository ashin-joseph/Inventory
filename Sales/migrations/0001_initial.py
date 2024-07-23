# Generated by Django 5.0.6 on 2024-07-23 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='salesorderItemTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soit_quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('soit_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('soit_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.itemtable')),
                ('soit_price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.pricetable')),
            ],
        ),
        migrations.CreateModel(
            name='salesorderTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sot_bill_number', models.CharField(max_length=20, unique=True)),
                ('sot_date', models.DateField(auto_now_add=True)),
                ('sot_items', models.ManyToManyField(through='Sales.salesorderItemTable', to='Core.itemtable')),
            ],
        ),
        migrations.AddField(
            model_name='salesorderitemtable',
            name='soit_bill_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sales.salesordertable'),
        ),
    ]
