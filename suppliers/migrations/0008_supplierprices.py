# Generated by Django 4.2.13 on 2024-05-25 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('suppliers', '0007_remove_suppliers_certifications_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierPrices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_exwb', models.FloatField(blank=True, null=True)),
                ('price_exws', models.FloatField(blank=True, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('suppliers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suppliers.suppliers')),
            ],
        ),
    ]