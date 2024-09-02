# Generated by Django 5.0.6 on 2024-09-02 06:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='damageTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dpt_damage_qty', models.PositiveIntegerField(blank=True, null=True)),
                ('dpt_timestamp', models.DateField(auto_now_add=True)),
                ('dpt_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.itemtable')),
            ],
        ),
    ]
