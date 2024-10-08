# Generated by Django 5.0.6 on 2024-09-10 06:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='stockTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('st_purchasesStock', models.PositiveIntegerField(default=0)),
                ('st_soldStock', models.PositiveIntegerField(default=0)),
                ('st_salesReturnStock', models.PositiveIntegerField(default=0)),
                ('st_damageStock', models.PositiveIntegerField(default=0)),
                ('st_remainingStock', models.PositiveIntegerField(default=0)),
                ('st_item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Core.itemtable')),
            ],
        ),
    ]
