# Generated by Django 4.2.13 on 2024-05-19 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offers',
            name='offer_price',
        ),
        migrations.AddField(
            model_name='offers',
            name='offer_f_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='offers',
            name='offer_m_price',
            field=models.FloatField(default=0),
        ),
    ]