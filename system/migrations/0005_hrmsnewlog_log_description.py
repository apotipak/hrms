# Generated by Django 3.0.7 on 2020-09-21 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_auto_20200918_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='hrmsnewlog',
            name='log_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]