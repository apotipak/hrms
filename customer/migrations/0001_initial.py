# Generated by Django 3.0.7 on 2020-09-17 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerOption',
            fields=[
                ('cus_no', models.DecimalField(db_column='CUS_NO', decimal_places=0, max_digits=10, primary_key=True, serialize=False)),
                ('btype', models.CharField(blank=True, db_column='Btype', max_length=100, null=True)),
                ('op1', models.CharField(blank=True, max_length=10, null=True)),
                ('op2', models.CharField(blank=True, max_length=100, null=True)),
                ('op3', models.CharField(blank=True, max_length=100, null=True)),
                ('op4', models.CharField(blank=True, max_length=100, null=True)),
                ('op5', models.CharField(blank=True, max_length=100, null=True)),
                ('op6', models.CharField(blank=True, max_length=100, null=True)),
                ('op7', models.CharField(blank=True, max_length=100, null=True)),
                ('op8', models.CharField(blank=True, max_length=100, null=True)),
                ('op9', models.CharField(blank=True, max_length=100, null=True)),
                ('op10', models.CharField(blank=True, max_length=100, null=True)),
                ('op11', models.CharField(blank=True, max_length=100, null=True)),
                ('op12', models.CharField(blank=True, max_length=100, null=True)),
                ('op13', models.CharField(blank=True, max_length=100, null=True)),
                ('op14', models.CharField(blank=True, max_length=100, null=True)),
                ('op15', models.CharField(blank=True, max_length=100, null=True)),
                ('opn1', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn2', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn3', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn4', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn5', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn6', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn7', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn8', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn9', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn10', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn11', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn12', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn13', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn14', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('opn15', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
            ],
            options={
                'db_table': 'Customer_option',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cus_no', models.DecimalField(decimal_places=0, max_digits=10, primary_key=True, serialize=False)),
                ('cus_id', models.DecimalField(decimal_places=0, max_digits=7)),
                ('cus_brn', models.DecimalField(decimal_places=0, max_digits=3)),
                ('cus_sht_th', models.CharField(blank=True, max_length=10, null=True)),
                ('cus_name_th', models.CharField(blank=True, max_length=120, null=True)),
                ('cus_add1_th', models.CharField(blank=True, max_length=150, null=True)),
                ('cus_add2_th', models.CharField(blank=True, max_length=70, null=True)),
                ('cus_subdist_th', models.CharField(blank=True, max_length=30, null=True)),
                ('cus_sht_en', models.CharField(blank=True, max_length=10, null=True)),
                ('cus_name_en', models.CharField(blank=True, max_length=120, null=True)),
                ('cus_add1_en', models.CharField(blank=True, max_length=150, null=True)),
                ('cus_add2_en', models.CharField(blank=True, max_length=70, null=True)),
                ('cus_subdist_en', models.CharField(blank=True, max_length=30, null=True)),
                ('cus_zip', models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True)),
                ('cus_tel', models.CharField(blank=True, max_length=40, null=True)),
                ('cus_fax', models.CharField(blank=True, max_length=30, null=True)),
                ('cus_email', models.CharField(blank=True, max_length=60, null=True)),
                ('cus_taxid', models.CharField(blank=True, max_length=30, null=True)),
                ('cus_active', models.BooleanField(blank=True, null=True)),
                ('cus_bill', models.BooleanField(blank=True, null=True)),
                ('cus_main', models.BooleanField(blank=True, null=True)),
                ('cus_site', models.BooleanField(blank=True, null=True)),
                ('last_contact', models.SmallIntegerField(blank=True, null=True)),
                ('upd_date', models.DateTimeField(blank=True, null=True)),
                ('upd_by', models.CharField(blank=True, max_length=10, null=True)),
                ('upd_flag', models.CharField(blank=True, max_length=1, null=True)),
                ('cus_city', models.ForeignKey(db_column='cus_city', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_site_cus_city_fk', to='system.TCity')),
                ('cus_contact', models.ForeignKey(db_column='cus_contact', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_site_cus_contact_fk', to='system.CusContact')),
                ('cus_country', models.ForeignKey(db_column='cus_country', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_site_t_country_fk', to='system.TCountry')),
                ('cus_district', models.ForeignKey(db_column='cus_district', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_site_t_district_fk', to='system.TDistrict')),
                ('cus_zone', models.ForeignKey(db_column='cus_zone', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_site_com_zone_fk', to='system.ComZone')),
                ('site_contact', models.ForeignKey(db_column='site_contact', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_site_site_contact_fk', to='system.CusContact')),
            ],
            options={
                'db_table': 'CUSTOMER',
                'ordering': ['cus_no'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CusMain',
            fields=[
                ('cus_id', models.DecimalField(decimal_places=0, max_digits=7, primary_key=True, serialize=False)),
                ('cus_sht_th', models.CharField(blank=True, max_length=10, null=True)),
                ('cus_name_th', models.CharField(blank=True, max_length=120, null=True)),
                ('cus_add1_th', models.CharField(blank=True, max_length=150, null=True)),
                ('cus_add2_th', models.CharField(blank=True, max_length=70, null=True)),
                ('cus_subdist_th', models.CharField(blank=True, max_length=50, null=True)),
                ('cus_sht_en', models.CharField(blank=True, max_length=10, null=True)),
                ('cus_name_en', models.CharField(blank=True, max_length=120, null=True)),
                ('cus_add1_en', models.CharField(blank=True, max_length=150, null=True)),
                ('cus_add2_en', models.CharField(blank=True, max_length=70, null=True)),
                ('cus_subdist_en', models.CharField(blank=True, max_length=50, null=True)),
                ('cus_zip', models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True)),
                ('cus_tel', models.CharField(blank=True, max_length=40, null=True)),
                ('cus_fax', models.CharField(blank=True, max_length=30, null=True)),
                ('cus_email', models.CharField(blank=True, max_length=60, null=True)),
                ('cus_taxid', models.CharField(blank=True, max_length=30, null=True)),
                ('cus_active', models.BooleanField(blank=True, null=True)),
                ('cus_bill', models.BooleanField(blank=True, null=True)),
                ('cus_main', models.BooleanField(blank=True, null=True)),
                ('cus_site', models.BooleanField(blank=True, null=True)),
                ('last_contact', models.SmallIntegerField(blank=True, null=True)),
                ('upd_date', models.DateTimeField(blank=True, null=True)),
                ('upd_by', models.CharField(blank=True, max_length=10, null=True)),
                ('upd_flag', models.CharField(blank=True, max_length=1, null=True)),
                ('cus_city', models.ForeignKey(db_column='cus_city', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_main_t_city_fk', to='system.TCity')),
                ('cus_contact', models.ForeignKey(db_column='cus_contact', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_main_cus_contact_fk', to='system.CusContact')),
                ('cus_country', models.ForeignKey(db_column='cus_country', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_main_t_country_fk', to='system.TCountry')),
                ('cus_district', models.ForeignKey(db_column='cus_district', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_main_t_district_fk', to='system.TDistrict')),
                ('cus_zone', models.ForeignKey(db_column='cus_zone', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_main_com_zone_fk', to='system.ComZone')),
                ('site_contact', models.ForeignKey(db_column='site_contact', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_main_site_contact_fk', to='system.CusContact')),
            ],
            options={
                'db_table': 'CUS_MAIN',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CusBill',
            fields=[
                ('cus_no', models.DecimalField(db_column='cus_no', decimal_places=0, max_digits=10, primary_key=True, serialize=False)),
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
                ('cus_zip', models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True)),
                ('cus_tel', models.CharField(blank=True, max_length=40, null=True)),
                ('cus_fax', models.CharField(blank=True, max_length=30, null=True)),
                ('cus_email', models.CharField(blank=True, max_length=50, null=True)),
                ('cus_taxid', models.CharField(blank=True, max_length=30, null=True)),
                ('cus_active', models.BooleanField(blank=True, null=True)),
                ('cus_bill', models.BooleanField(blank=True, null=True)),
                ('cus_main', models.BooleanField(blank=True, null=True)),
                ('cus_site', models.BooleanField(blank=True, null=True)),
                ('last_contact', models.SmallIntegerField(blank=True, null=True)),
                ('upd_date', models.DateTimeField(blank=True, null=True)),
                ('upd_by', models.CharField(blank=True, max_length=10, null=True)),
                ('upd_flag', models.CharField(blank=True, max_length=1, null=True)),
                ('cus_city', models.ForeignKey(db_column='cus_city_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_bill_t_city_fk', to='system.TCity')),
                ('cus_contact', models.ForeignKey(db_column='cus_contact', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_bill_cus_contact_fk', to='system.CusContact')),
                ('cus_country', models.ForeignKey(db_column='cus_country', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_bill_t_country_fk', to='system.TCountry')),
                ('cus_district', models.ForeignKey(db_column='cus_district', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_bill_t_district_fk', to='system.TDistrict')),
                ('cus_zone', models.ForeignKey(db_column='cus_zone', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_bill_cus_com_zone_fk', to='system.ComZone')),
                ('site_contact', models.ForeignKey(db_column='site_contact', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus_bill_site_contact_fk', to='system.CusContact')),
            ],
            options={
                'db_table': 'CUS_BILL',
                'managed': True,
            },
        ),
    ]
