# Generated by Django 3.0.7 on 2020-09-21 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_hrmsnewlog_log_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hrmsnewlog',
            old_name='log_key',
            new_name='log_table_name',
        ),
    ]