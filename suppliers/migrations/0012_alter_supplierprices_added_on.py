# Generated by Django 3.2.4 on 2024-06-07 18:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0011_alter_suppliers_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierprices',
            name='added_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]