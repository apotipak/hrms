# Generated by Django 3.0.7 on 2020-07-20 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20200310_0801'),
    ]

    operations = [
        migrations.CreateModel(
            name='TDistrict',
            fields=[
                ('dist_id', models.DecimalField(decimal_places=0, max_digits=4, primary_key=True, serialize=False)),
                ('city_id', models.DecimalField(blank=True, decimal_places=0, max_digits=2, null=True)),
                ('dist_th', models.CharField(blank=True, max_length=30, null=True)),
                ('dist_en', models.CharField(blank=True, max_length=30, null=True)),
                ('upd_date', models.DateTimeField(blank=True, null=True)),
                ('upd_by', models.CharField(blank=True, max_length=10, null=True)),
                ('upd_flag', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'db_table': 'T_DISTRICT',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'managed': True, 'ordering': ['cus_no']},
        ),
    ]
