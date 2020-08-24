# Generated by Django 3.0.7 on 2020-08-24 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='cus_zone',
            field=models.ForeignKey(db_column='cus_zone', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_zone', to='system.ComZone'),
        ),
    ]
