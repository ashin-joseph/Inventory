# Generated by Django 5.0.6 on 2024-08-21 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_companyprofiletable'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyprofiletable',
            name='company_Purchase_note',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='companyprofiletable',
            name='company_Sales_note',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
