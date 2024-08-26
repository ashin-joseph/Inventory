# Generated by Django 5.0.6 on 2024-08-26 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Purchase', '0004_alter_confirmpurchaseitemtable_cpit_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='cpt_backup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpt_b_billNum', models.CharField(max_length=50, unique=True)),
                ('cpt_b_vendor', models.CharField(blank=True, max_length=100, null=True)),
                ('cpt_b_address', models.CharField(blank=True, max_length=100, null=True)),
                ('cpt_b_gst', models.CharField(blank=True, max_length=100, null=True)),
                ('cpt_b_contact', models.CharField(blank=True, max_length=100, null=True)),
                ('cpt_b_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('cpt_b_date', models.CharField(blank=True, max_length=100, null=True)),
                ('cpt_b_user', models.CharField(blank=True, max_length=100, null=True)),
                ('cpt_b_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='confirmpurchasetable',
            name='cpt_billNum',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='ordertable',
            name='ot_order_number',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.CreateModel(
            name='cpit_backup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpit_b_item', models.CharField(blank=True, max_length=100, null=True)),
                ('cpit_b_qty', models.PositiveIntegerField(blank=True, null=True)),
                ('cpit_b_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cpit_b_tax', models.PositiveIntegerField(blank=True, null=True)),
                ('cpit_b_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cpit_b_billNum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Purchase.cpt_backup')),
            ],
        ),
    ]
