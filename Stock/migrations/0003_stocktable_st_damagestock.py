# Generated by Django 5.0.6 on 2024-07-05 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0002_alter_stocktable_st_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocktable',
            name='st_damageStock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
