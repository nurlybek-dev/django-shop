# Generated by Django 3.1.7 on 2021-03-09 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210309_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='contact_phone',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.CharField(max_length=255),
        ),
    ]
