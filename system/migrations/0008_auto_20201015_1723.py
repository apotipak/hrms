# Generated by Django 3.1.2 on 2020-10-15 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_tnation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuscontact',
            name='con_nation',
            field=models.ForeignKey(db_column='con_nation', null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.tnation'),
        ),
    ]
