# Generated by Django 3.0.7 on 2020-09-17 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_delete_hrmsnewlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='HrmsNewLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_id', models.IntegerField(db_column='Log_ID')),
                ('log_date', models.DateTimeField(auto_now_add=True, db_column='Log_Date')),
                ('log_emptype', models.CharField(blank=True, db_column='Log_EmpType', max_length=50, null=True)),
                ('log_empid', models.DecimalField(blank=True, db_column='Log_EmpID', decimal_places=0, max_digits=15, null=True)),
                ('log_desc', models.CharField(blank=True, db_column='Log_Desc', max_length=500, null=True)),
                ('log_type', models.CharField(blank=True, db_column='Log_Type', max_length=1, null=True)),
                ('upd_by', models.CharField(blank=True, db_column='Upd_By', max_length=20, null=True)),
                ('upd_date', models.DateTimeField(auto_now_add=True, db_column='Upd_Date', null=True)),
            ],
            options={
                'db_table': 'hrms_new_log',
                'managed': True,
                'unique_together': {('log_id', 'log_date')},
            },
        ),
    ]
