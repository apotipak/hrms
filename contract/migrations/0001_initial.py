# Generated by Django 3.0.7 on 2020-08-03 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('system', '0004_groupbill'),
    ]

    operations = [
        migrations.CreateModel(
            name='CusContract',
            fields=[
                ('cnt_id', models.DecimalField(decimal_places=0, max_digits=13, primary_key=True, serialize=False)),
                ('cus_id', models.DecimalField(blank=True, decimal_places=0, max_digits=7, null=True)),
                ('cus_brn', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('cus_vol', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('cnt_active', models.BooleanField(blank=True, null=True)),
                ('cnt_sign_frm', models.DateTimeField(blank=True, null=True)),
                ('cnt_sign_to', models.DateTimeField(blank=True, null=True)),
                ('cnt_eff_frm', models.DateTimeField(blank=True, null=True)),
                ('cnt_eff_to', models.DateTimeField(blank=True, null=True)),
                ('cnt_doc_no', models.CharField(blank=True, max_length=25, null=True)),
                ('cnt_doc_date', models.DateTimeField(blank=True, null=True)),
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
                ('cnt_apr_by', models.ForeignKey(db_column='cnt_apr_by', null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.TAprove')),
            ],
            options={
                'db_table': 'CUS_CONTRACT',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CusService',
            fields=[
                ('srv_id', models.DecimalField(decimal_places=0, max_digits=16, primary_key=True, serialize=False)),
                ('srv_rank', models.CharField(blank=True, max_length=3, null=True)),
                ('srv_shif_id', models.SmallIntegerField(blank=True, null=True)),
                ('srv_eff_frm', models.DateTimeField(blank=True, null=True)),
                ('srv_eff_to', models.DateTimeField(blank=True, null=True)),
                ('srv_qty', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('srv_mon', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('srv_tue', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('srv_wed', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('srv_thu', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('srv_fri', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('srv_sat', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('srv_sun', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('srv_pub', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('srv_active', models.BooleanField(blank=True, null=True)),
                ('srv_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('srv_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('srv_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('upd_date', models.DateTimeField(blank=True, null=True)),
                ('upd_by', models.CharField(blank=True, max_length=10, null=True)),
                ('upd_flag', models.CharField(blank=True, max_length=1, null=True)),
                ('srv_cost_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('srv_cost_change', models.CharField(blank=True, db_column='Srv_cost_change', max_length=1, null=True)),
                ('op1', models.CharField(blank=True, max_length=10, null=True)),
                ('op2', models.CharField(blank=True, max_length=10, null=True)),
                ('op3', models.CharField(blank=True, max_length=10, null=True)),
                ('cnt_id', models.ForeignKey(db_column='cnt_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contract.CusContract')),
            ],
            options={
                'db_table': 'CUS_SERVICE',
                'managed': True,
            },
        ),
    ]
