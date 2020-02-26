from django.db import models

class TAprove(models.Model):
    apr_id = models.DecimalField(primary_key=True, max_digits=6, decimal_places=0)
    apr_title = models.SmallIntegerField(blank=True, null=True)
    apr_name_th = models.CharField(max_length=60, blank=True, null=True)
    apr_name_en = models.CharField(max_length=60, blank=True, null=True)
    apr_pos_th = models.CharField(max_length=50, blank=True, null=True)
    apr_pos_en = models.CharField(max_length=50, blank=True, null=True)
    apr_piority = models.CharField(max_length=3, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_APROVE'



class TTitle(models.Model):
    title_id = models.SmallIntegerField(primary_key=True)
    title_th = models.CharField(max_length=30, blank=True, null=True)
    title_en = models.CharField(max_length=30, blank=True, null=True)
    title_sht_th = models.CharField(max_length=10, blank=True, null=True)
    title_sht_en = models.CharField(max_length=10, blank=True, null=True)
    title_sex = models.CharField(max_length=1, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_TITLE'


class Company(models.Model):
    com_id = models.DecimalField(primary_key=True, max_digits=2, decimal_places=0)
    com_sht_th = models.CharField(max_length=10, blank=True, null=True)
    com_name_th = models.CharField(max_length=80, blank=True, null=True)
    com_add1_th = models.CharField(max_length=50, blank=True, null=True)
    com_add2_th = models.CharField(max_length=50, blank=True, null=True)
    com_subdist_th = models.CharField(max_length=20, blank=True, null=True)
    com_sht_en = models.CharField(max_length=10, blank=True, null=True)
    com_name_en = models.CharField(max_length=80, blank=True, null=True)
    com_add1_en = models.CharField(max_length=50, blank=True, null=True)
    com_add2_en = models.CharField(max_length=50, blank=True, null=True)
    com_subdist_en = models.CharField(max_length=20, blank=True, null=True)
    com_district = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    com_city = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    com_country = models.SmallIntegerField(blank=True, null=True)
    com_zip = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    com_tel1 = models.CharField(max_length=15, blank=True, null=True)
    com_tel2 = models.CharField(max_length=15, blank=True, null=True)
    com_fax1 = models.CharField(max_length=15, blank=True, null=True)
    com_fax2 = models.CharField(max_length=15, blank=True, null=True)
    com_email = models.CharField(max_length=20, blank=True, null=True)
    com_taxid = models.CharField(max_length=13, blank=True, null=True)
    com_socid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    com_brnid = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    com_soc_no = models.CharField(max_length=2, blank=True, null=True)
    com_soc_brn = models.CharField(max_length=6, blank=True, null=True)
    com_active = models.BooleanField(blank=True, null=True)
    com_main = models.BooleanField(blank=True, null=True)
    com_parent = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    com_hr_month = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    com_hr_day = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    com_md = models.DecimalField(db_column='com_MD', max_digits=7, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    com_admin = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    com_hr = models.DecimalField(db_column='com_HR', max_digits=7, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    com_acno = models.CharField(max_length=12, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'COMPANY'
