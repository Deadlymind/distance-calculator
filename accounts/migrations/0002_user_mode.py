# Generated by Django 3.2.4 on 2024-05-08 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mode',
            field=models.CharField(choices=[('sourcing', 'Sourcing'), ('sales', 'Sales')], default='sourcing', max_length=10),
        ),
    ]