# Generated by Django 3.0.7 on 2020-07-20 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0010_tdistrict'),
    ]

    operations = [
        migrations.CreateModel(
            name='CusContact',
            fields=[
                ('con_id', models.DecimalField(decimal_places=0, max_digits=10, primary_key=True, serialize=False)),
                ('cus_id', models.DecimalField(decimal_places=0, max_digits=7)),
                ('cus_brn', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('cus_rem', models.CharField(blank=True, max_length=10, null=True)),
                ('con_type', models.CharField(blank=True, max_length=1, null=True)),
                ('con_title', models.SmallIntegerField(blank=True, null=True)),
                ('con_fname_th', models.CharField(blank=True, max_length=70, null=True)),
                ('con_lname_th', models.CharField(blank=True, max_length=40, null=True)),
                ('con_position_th', models.CharField(blank=True, max_length=80, null=True)),
                ('con_fname_en', models.CharField(blank=True, max_length=70, null=True)),
                ('con_lname_en', models.CharField(blank=True, max_length=40, null=True)),
                ('con_position_en', models.CharField(blank=True, max_length=80, null=True)),
                ('con_nation', models.SmallIntegerField(blank=True, null=True)),
                ('con_sex', models.CharField(blank=True, max_length=1, null=True)),
                ('con_mobile', models.CharField(blank=True, max_length=30, null=True)),
                ('con_email', models.CharField(blank=True, max_length=70, null=True)),
                ('upd_date', models.DateTimeField(blank=True, null=True)),
                ('upd_by', models.CharField(blank=True, max_length=10, null=True)),
                ('upd_flag', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'db_table': 'CUS_CONTACT',
                'managed': False,
            },
        ),
    ]
