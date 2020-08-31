# Generated by Django 3.0.7 on 2020-08-27 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20200826_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cus_no', models.DecimalField(db_column='CUS_NO', decimal_places=0, max_digits=10)),
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
                'managed': False,
            },
        ),
    ]