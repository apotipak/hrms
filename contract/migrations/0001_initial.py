# Generated by Django 2.2.10 on 2020-03-19 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0002_auto_20200310_0801'),
    ]

    operations = [
        migrations.CreateModel(
            name='CusContract',
            fields=[
                ('cnt_id', models.DecimalField(decimal_places=0, max_digits=13, primary_key=True, serialize=False)),
                ('cus_id', models.ForeignKey(db_column='cus_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.Customer')),
                ('cus_brn', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('cus_vol', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('cnt_active', models.BooleanField(blank=True, null=True)),
                ('cnt_sign_frm', models.DateTimeField(blank=True, null=True)),
                ('cnt_sign_to', models.DateTimeField(blank=True, null=True)),
                ('cnt_eff_frm', models.DateTimeField(blank=True, null=True)),
                ('cnt_eff_to', models.DateTimeField(blank=True, null=True)),
                ('cnt_doc_no', models.CharField(blank=True, max_length=25, null=True)),
                ('cnt_doc_date', models.DateTimeField(blank=True, null=True)),
                ('cnt_apr_by', models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True)),
                ('cnt_guard_amt', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('cnt_sale_amt', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cnt_wage_id', models.DecimalField(blank=True, decimal_places=0, max_digits=2, null=True)),
                ('cnt_zone', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('cnt_autoexpire', models.BooleanField(blank=True, null=True)),
                ('cnt_then', models.CharField(blank=True, max_length=1, null=True)),
                ('cnt_print', models.CharField(blank=True, max_length=1, null=True)),
                ('cnt_new', models.CharField(blank=True, max_length=1, null=True)),
                ('upd_date', models.DateTimeField(blank=True, null=True)),
                ('upd_by', models.CharField(blank=True, max_length=10, null=True)),
                ('upd_flag', models.CharField(blank=True, max_length=1, null=True)),
                ('b_cnt_eff_frm', models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True)),
                ('b_cnt_eff_to', models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True)),
                ('b_cnt_loc', models.CharField(blank=True, max_length=200, null=True)),
                ('b_cnt_sign_frm', models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True)),
                ('b_cnt_sign_to', models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True)),
                ('b_siteno', models.CharField(blank=True, max_length=10, null=True)),
                ('cus_rewrite', models.DateTimeField(blank=True, null=True)),                
            ],
            options={
                'db_table': 'CUS_CONTRACT',
                'managed': True,
            },
        ),
    ]
