# Generated by Django 3.1.7 on 2021-03-12 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20210312_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='comment',
            field=models.TextField(blank=True, default=''),
        ),
    ]
