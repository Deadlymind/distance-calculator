# Generated by Django 4.2.13 on 2024-05-18 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('suppliers', '0005_rename_final_price_suppliers_price_exwb_and_more'),
        ('countries', '0005_regions_center_lat_regions_center_lng'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('road_distance_price', models.FloatField()),
                ('price_exwb', models.FloatField()),
                ('price_exws', models.FloatField()),
                ('weight', models.FloatField()),
                ('offer_price', models.FloatField()),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='countries.regions')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suppliers.suppliers')),
            ],
        ),
    ]