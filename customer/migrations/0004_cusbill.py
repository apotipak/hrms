# Generated by Django 3.0.7 on 2020-08-05 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20200803_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='CusBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cus_no', models.DecimalField(decimal_places=0, max_digits=10)),
                ('cus_id', models.DecimalField(decimal_places=0, max_digits=7)),
                ('cus_brn', models.DecimalField(decimal_places=0, max_digits=3)),
                ('cus_sht_th', models.CharField(blank=True, max_length=10, null=True)),
                ('cus_name_th', models.CharField(blank=True, max_length=120, null=True)),
                ('cus_add1_th', models.CharField(blank=True, max_length=200, null=True)),
                ('cus_add2_th', models.CharField(blank=True, max_length=200, null=True)),
                ('cus_subdist_th', models.CharField(blank=True, max_length=100, null=True)),
                ('cus_sht_en', models.CharField(blank=True, max_length=10, null=True)),
                ('cus_name_en', models.CharField(blank=True, max_length=120, null=True)),
                ('cus_add1_en', models.CharField(blank=True, max_length=200, null=True)),
                ('cus_add2_en', models.CharField(blank=True, max_length=200, null=True)),
                ('cus_subdist_en', models.CharField(blank=True, max_length=100, null=True)),
                ('cus_district', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('cus_city', models.DecimalField(blank=True, decimal_places=0, max_digits=2, null=True)),
                ('cus_country', models.SmallIntegerField(blank=True, null=True)),
                ('cus_zip', models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True)),
                ('cus_tel', models.CharField(blank=True, max_length=40, null=True)),
                ('cus_fax', models.CharField(blank=True, max_length=30, null=True)),
                ('cus_email', models.CharField(blank=True, max_length=50, null=True)),
                ('cus_taxid', models.CharField(blank=True, max_length=30, null=True)),
                ('cus_active', models.BooleanField(blank=True, null=True)),
                ('cus_bill', models.BooleanField(blank=True, null=True)),
                ('cus_main', models.BooleanField(blank=True, null=True)),
                ('cus_site', models.BooleanField(blank=True, null=True)),
                ('cus_zone', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('cus_contact', models.DecimalField(blank=True, decimal_places=0, max_digits=7, null=True)),
                ('site_contact', models.DecimalField(blank=True, decimal_places=0, max_digits=7, null=True)),
                ('last_contact', models.SmallIntegerField(blank=True, null=True)),
                ('upd_date', models.DateTimeField(blank=True, null=True)),
                ('upd_by', models.CharField(blank=True, max_length=10, null=True)),
                ('upd_flag', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'db_table': 'CUS_BILL',
                'managed': True,
            },
        ),
    ]
