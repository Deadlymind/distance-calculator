# Generated by Django 3.2.4 on 2024-05-11 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='regions',
            name='coefficient_distance',
            field=models.FloatField(default=100),
        ),
        migrations.AddField(
            model_name='regions',
            name='cofficient_price',
            field=models.FloatField(default=1.1),
        ),
    ]