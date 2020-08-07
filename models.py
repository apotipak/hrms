# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Arcode(models.Model):
    cnt_id = models.FloatField(db_column='Cnt_id', blank=True, null=True)  # Field name made lowercase.
    arcode = models.FloatField(db_column='ARCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ARcode'


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


class ComDepartment(models.Model):
    dept_id = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    div_id = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    dept_sht = models.CharField(max_length=20, blank=True, null=True)
    dept_th = models.CharField(max_length=50, blank=True, null=True)
    dept_en = models.CharField(max_length=50, blank=True, null=True)
    dept_zone = models.BooleanField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'COM_DEPARTMENT'


class ComDivision(models.Model):
    div_id = models.DecimalField(primary_key=True, max_digits=3, decimal_places=0)
    com_id = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    div_th = models.CharField(max_length=50, blank=True, null=True)
    div_en = models.CharField(max_length=50, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'COM_DIVISION'


class ComPosition(models.Model):
    pos_id = models.SmallIntegerField(primary_key=True)
    pos_sht = models.CharField(max_length=10, blank=True, null=True)
    pos_th = models.CharField(max_length=50, blank=True, null=True)
    pos_en = models.CharField(max_length=50, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'COM_POSITION'


class ComRank(models.Model):
    rank_id = models.CharField(primary_key=True, max_length=3)
    rank_th = models.CharField(max_length=30, blank=True, null=True)
    rank_en = models.CharField(max_length=30, blank=True, null=True)
    rank_type = models.CharField(max_length=3, blank=True, null=True)
    rank_start = models.DateTimeField(blank=True, null=True)
    rank_grd = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    rank_promot = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'COM_RANK'


class ComSection(models.Model):
    sect_id = models.DecimalField(primary_key=True, max_digits=8, decimal_places=0)
    dept_id = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    sect_th = models.CharField(max_length=50, blank=True, null=True)
    sect_en = models.CharField(max_length=50, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'COM_SECTION'


class ComType(models.Model):
    com_type = models.CharField(primary_key=True, max_length=2)
    com_id = models.SmallIntegerField(blank=True, null=True)
    type_des = models.CharField(max_length=30, blank=True, null=True)
    type_th = models.CharField(max_length=30, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'COM_TYPE'


class ComZone(models.Model):
    zone_id = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    zone_th = models.CharField(max_length=30, blank=True, null=True)
    zone_en = models.CharField(max_length=30, blank=True, null=True)
    zone_emp_id = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'COM_ZONE'


class Customer(models.Model):
    cus_no = models.DecimalField(max_digits=10, decimal_places=0)
    cus_id = models.DecimalField(max_digits=7, decimal_places=0)
    cus_brn = models.DecimalField(max_digits=3, decimal_places=0)
    cus_sht_th = models.CharField(max_length=10, blank=True, null=True)
    cus_name_th = models.CharField(max_length=120, blank=True, null=True)
    cus_add1_th = models.CharField(max_length=150, blank=True, null=True)
    cus_add2_th = models.CharField(max_length=70, blank=True, null=True)
    cus_subdist_th = models.CharField(max_length=30, blank=True, null=True)
    cus_sht_en = models.CharField(max_length=10, blank=True, null=True)
    cus_name_en = models.CharField(max_length=120, blank=True, null=True)
    cus_add1_en = models.CharField(max_length=150, blank=True, null=True)
    cus_add2_en = models.CharField(max_length=70, blank=True, null=True)
    cus_subdist_en = models.CharField(max_length=30, blank=True, null=True)
    cus_district = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    cus_city = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    cus_country = models.SmallIntegerField(blank=True, null=True)
    cus_zip = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    cus_tel = models.CharField(max_length=40, blank=True, null=True)
    cus_fax = models.CharField(max_length=30, blank=True, null=True)
    cus_email = models.CharField(max_length=60, blank=True, null=True)
    cus_taxid = models.CharField(max_length=30, blank=True, null=True)
    cus_active = models.BooleanField(blank=True, null=True)
    cus_bill = models.BooleanField(blank=True, null=True)
    cus_main = models.BooleanField(blank=True, null=True)
    cus_site = models.BooleanField(blank=True, null=True)
    cus_zone = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    cus_contact = models.ForeignKey('CusContact', models.DO_NOTHING, db_column='cus_contact', blank=True, null=True)
    site_contact = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    last_contact = models.SmallIntegerField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CUSTOMER'


class CusBill(models.Model):
    cus_no = models.DecimalField(max_digits=10, decimal_places=0)
    cus_id = models.DecimalField(max_digits=7, decimal_places=0)
    cus_brn = models.DecimalField(max_digits=3, decimal_places=0)
    cus_sht_th = models.CharField(max_length=10, blank=True, null=True)
    cus_name_th = models.CharField(max_length=120, blank=True, null=True)
    cus_add1_th = models.CharField(max_length=200, blank=True, null=True)
    cus_add2_th = models.CharField(max_length=200, blank=True, null=True)
    cus_subdist_th = models.CharField(max_length=100, blank=True, null=True)
    cus_sht_en = models.CharField(max_length=10, blank=True, null=True)
    cus_name_en = models.CharField(max_length=120, blank=True, null=True)
    cus_add1_en = models.CharField(max_length=200, blank=True, null=True)
    cus_add2_en = models.CharField(max_length=200, blank=True, null=True)
    cus_subdist_en = models.CharField(max_length=100, blank=True, null=True)
    cus_district = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    cus_city = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    cus_country = models.SmallIntegerField(blank=True, null=True)
    cus_zip = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    cus_tel = models.CharField(max_length=40, blank=True, null=True)
    cus_fax = models.CharField(max_length=30, blank=True, null=True)
    cus_email = models.CharField(max_length=50, blank=True, null=True)
    cus_taxid = models.CharField(max_length=30, blank=True, null=True)
    cus_active = models.BooleanField(blank=True, null=True)
    cus_bill = models.BooleanField(blank=True, null=True)
    cus_main = models.BooleanField(blank=True, null=True)
    cus_site = models.BooleanField(blank=True, null=True)
    cus_zone = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    cus_contact = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    site_contact = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    last_contact = models.SmallIntegerField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CUS_BILL'


class CusContact(models.Model):
    con_id = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    cus_id = models.DecimalField(max_digits=7, decimal_places=0)
    cus_brn = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    cus_rem = models.CharField(max_length=10, blank=True, null=True)
    con_type = models.CharField(max_length=1, blank=True, null=True)
    con_title = models.SmallIntegerField(blank=True, null=True)
    con_fname_th = models.CharField(max_length=70, blank=True, null=True)
    con_lname_th = models.CharField(max_length=40, blank=True, null=True)
    con_position_th = models.CharField(max_length=80, blank=True, null=True)
    con_fname_en = models.CharField(max_length=70, blank=True, null=True)
    con_lname_en = models.CharField(max_length=40, blank=True, null=True)
    con_position_en = models.CharField(max_length=80, blank=True, null=True)
    con_nation = models.SmallIntegerField(blank=True, null=True)
    con_sex = models.CharField(max_length=1, blank=True, null=True)
    con_mobile = models.CharField(max_length=30, blank=True, null=True)
    con_email = models.CharField(max_length=70, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CUS_CONTACT'


class CusContract(models.Model):
    cnt_id = models.DecimalField(primary_key=True, max_digits=13, decimal_places=0)
    cus_id = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    cus_brn = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    cus_vol = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    cnt_active = models.BooleanField(blank=True, null=True)
    cnt_sign_frm = models.DateTimeField(blank=True, null=True)
    cnt_sign_to = models.DateTimeField(blank=True, null=True)
    cnt_eff_frm = models.DateTimeField(blank=True, null=True)
    cnt_eff_to = models.DateTimeField(blank=True, null=True)
    cnt_doc_no = models.CharField(max_length=25, blank=True, null=True)
    cnt_doc_date = models.DateTimeField(blank=True, null=True)
    cnt_apr_by = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    cnt_guard_amt = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    cnt_sale_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cnt_wage = models.ForeignKey('TWagezone', models.DO_NOTHING, blank=True, null=True)
    cnt_zone = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    cnt_autoexpire = models.BooleanField(blank=True, null=True)
    cnt_then = models.CharField(max_length=1, blank=True, null=True)
    cnt_print = models.CharField(max_length=1, blank=True, null=True)
    cnt_new = models.CharField(max_length=1, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)
    b_cnt_eff_frm = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    b_cnt_eff_to = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    b_cnt_loc = models.CharField(max_length=200, blank=True, null=True)
    b_cnt_sign_frm = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    b_cnt_sign_to = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    b_siteno = models.CharField(max_length=10, blank=True, null=True)
    cus_rewrite = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CUS_CONTRACT'


class CusGroup(models.Model):
    gname = models.CharField(db_column='Gname', primary_key=True, max_length=30)  # Field name made lowercase.
    gcode = models.CharField(db_column='Gcode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    upd = models.DateTimeField(db_column='Upd', blank=True, null=True)  # Field name made lowercase.
    upd_flag = models.CharField(db_column='Upd_flag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    upd_by = models.CharField(db_column='Upd_By', max_length=30, blank=True, null=True)  # Field name made lowercase.
    op1 = models.CharField(max_length=10, blank=True, null=True)
    op2 = models.CharField(max_length=10, blank=True, null=True)
    op3 = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CUS_GROUP'


class CusMain(models.Model):
    cus_id = models.DecimalField(primary_key=True, max_digits=7, decimal_places=0)
    cus_sht_th = models.CharField(max_length=10, blank=True, null=True)
    cus_name_th = models.CharField(max_length=120, blank=True, null=True)
    cus_add1_th = models.CharField(max_length=150, blank=True, null=True)
    cus_add2_th = models.CharField(max_length=70, blank=True, null=True)
    cus_subdist_th = models.CharField(max_length=50, blank=True, null=True)
    cus_sht_en = models.CharField(max_length=10, blank=True, null=True)
    cus_name_en = models.CharField(max_length=120, blank=True, null=True)
    cus_add1_en = models.CharField(max_length=150, blank=True, null=True)
    cus_add2_en = models.CharField(max_length=70, blank=True, null=True)
    cus_subdist_en = models.CharField(max_length=50, blank=True, null=True)
    cus_district = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    cus_city = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    cus_country = models.SmallIntegerField(blank=True, null=True)
    cus_zip = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    cus_tel = models.CharField(max_length=40, blank=True, null=True)
    cus_fax = models.CharField(max_length=30, blank=True, null=True)
    cus_email = models.CharField(max_length=60, blank=True, null=True)
    cus_taxid = models.CharField(max_length=30, blank=True, null=True)
    cus_active = models.BooleanField(blank=True, null=True)
    cus_bill = models.BooleanField(blank=True, null=True)
    cus_main = models.BooleanField(blank=True, null=True)
    cus_site = models.BooleanField(blank=True, null=True)
    cus_zone = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    cus_contact = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    site_contact = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    last_contact = models.SmallIntegerField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CUS_MAIN'


class CusService(models.Model):
    srv_id = models.DecimalField(primary_key=True, max_digits=16, decimal_places=0)
    cnt_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    srv_rank = models.CharField(max_length=3, blank=True, null=True)
    srv_shif_id = models.SmallIntegerField(blank=True, null=True)
    srv_eff_frm = models.DateTimeField(blank=True, null=True)
    srv_eff_to = models.DateTimeField(blank=True, null=True)
    srv_qty = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    srv_mon = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    srv_tue = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    srv_wed = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    srv_thu = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    srv_fri = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    srv_sat = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    srv_sun = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    srv_pub = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    srv_active = models.BooleanField(blank=True, null=True)
    srv_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    srv_cost = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    srv_rem = models.CharField(max_length=100, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)
    srv_cost_rate = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    srv_cost_change = models.CharField(db_column='Srv_cost_change', max_length=1, blank=True, null=True)  # Field name made lowercase.
    op1 = models.CharField(max_length=10, blank=True, null=True)
    op2 = models.CharField(max_length=10, blank=True, null=True)
    op3 = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CUS_SERVICE'


class ContractShfQty(models.Model):
    cnt_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    cus_name_en = models.CharField(max_length=120, blank=True, null=True)
    cus_name_th = models.CharField(max_length=120, blank=True, null=True)
    zone_en = models.CharField(max_length=30, blank=True, null=True)
    cnt_zone = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    shf_type = models.CharField(max_length=1, blank=True, null=True)
    qty = models.DecimalField(db_column='QTY', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Contract_Shf_qty'


class ContractSumShfQty(models.Model):
    cnt_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    cus_name_en = models.CharField(max_length=120, blank=True, null=True)
    cus_name_th = models.CharField(max_length=120, blank=True, null=True)
    zone_en = models.CharField(max_length=30, blank=True, null=True)
    cnt_zone = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    d = models.DecimalField(db_column='D', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    n = models.DecimalField(db_column='N', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Contract_sum_Shf_qty'


class CustomerOption(models.Model):
    cus_no = models.DecimalField(db_column='CUS_NO', max_digits=10, decimal_places=0)  # Field name made lowercase.
    btype = models.CharField(db_column='Btype', max_length=100, blank=True, null=True)  # Field name made lowercase.
    op1 = models.CharField(max_length=10, blank=True, null=True)
    op2 = models.CharField(max_length=100, blank=True, null=True)
    op3 = models.CharField(max_length=100, blank=True, null=True)
    op4 = models.CharField(max_length=100, blank=True, null=True)
    op5 = models.CharField(max_length=100, blank=True, null=True)
    op6 = models.CharField(max_length=100, blank=True, null=True)
    op7 = models.CharField(max_length=100, blank=True, null=True)
    op8 = models.CharField(max_length=100, blank=True, null=True)
    op9 = models.CharField(max_length=100, blank=True, null=True)
    op10 = models.CharField(max_length=100, blank=True, null=True)
    op11 = models.CharField(max_length=100, blank=True, null=True)
    op12 = models.CharField(max_length=100, blank=True, null=True)
    op13 = models.CharField(max_length=100, blank=True, null=True)
    op14 = models.CharField(max_length=100, blank=True, null=True)
    op15 = models.CharField(max_length=100, blank=True, null=True)
    opn1 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn2 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn3 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn4 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn5 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn6 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn7 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn8 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn9 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn10 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn11 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn12 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn13 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn14 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opn15 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Customer_option'


class DlyPlan(models.Model):
    cnt_id = models.DecimalField(primary_key=True, max_digits=13, decimal_places=0)
    emp_id = models.DecimalField(max_digits=7, decimal_places=0)
    dly_date = models.DateTimeField()
    sch_shift = models.DecimalField(max_digits=4, decimal_places=0)
    sch_no = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True)
    dept_id = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    sch_rank = models.CharField(max_length=3, blank=True, null=True)
    prd_id = models.CharField(max_length=7, blank=True, null=True)
    absent = models.BooleanField(blank=True, null=True)
    late = models.BooleanField(blank=True, null=True)
    late_full = models.BooleanField(blank=True, null=True)
    sch_relieft = models.BooleanField(blank=True, null=True)
    relieft = models.BooleanField(blank=True, null=True)
    relieft_id = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    tel_man = models.BooleanField(blank=True, null=True)
    tel_time = models.DateTimeField(blank=True, null=True)
    tel_amt = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    tel_paid = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    ot = models.BooleanField(blank=True, null=True)
    ot_reason = models.SmallIntegerField(blank=True, null=True)
    ot_time_frm = models.DateTimeField(blank=True, null=True)
    ot_time_to = models.DateTimeField(blank=True, null=True)
    ot_hr_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ot_pay_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    spare = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    wage_id = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    wage_no = models.CharField(max_length=5, blank=True, null=True)
    pay_type = models.CharField(max_length=3, blank=True, null=True)
    bas_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    otm_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bon_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pub_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    soc_amt = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    dof_amt = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    ex_dof_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    soc = models.BooleanField(blank=True, null=True)
    pub = models.BooleanField(blank=True, null=True)
    dof = models.BooleanField(blank=True, null=True)
    paid = models.BooleanField(blank=True, null=True)
    tpa = models.BooleanField(db_column='TPA', blank=True, null=True)  # Field name made lowercase.
    day7 = models.BooleanField(db_column='DAY7', blank=True, null=True)  # Field name made lowercase.
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)
    upd_gen = models.CharField(max_length=1, blank=True, null=True)
    upd_log = models.TextField(blank=True, null=True)  # This field type is a guess.
    remark = models.CharField(db_column='Remark', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DLY_PLAN'
        unique_together = (('cnt_id', 'emp_id', 'dly_date', 'sch_shift'),)


class Employee(models.Model):
    emp_id = models.DecimalField(max_digits=7, decimal_places=0)
    emp_title = models.SmallIntegerField()
    emp_fname_en = models.CharField(max_length=30, blank=True, null=True)
    emp_lname_en = models.CharField(max_length=40, blank=True, null=True)
    emp_fname_th = models.CharField(max_length=30, blank=True, null=True)
    emp_lname_th = models.CharField(max_length=40, blank=True, null=True)
    emp_birth = models.DateTimeField(blank=True, null=True)
    emp_age = models.SmallIntegerField(blank=True, null=True)
    emp_sex = models.CharField(max_length=1, blank=True, null=True)
    emp_scar_th = models.CharField(max_length=30, blank=True, null=True)
    emp_scar_en = models.CharField(max_length=30, blank=True, null=True)
    emp_race = models.SmallIntegerField(blank=True, null=True)
    emp_nation = models.SmallIntegerField(blank=True, null=True)
    emp_religion = models.SmallIntegerField(blank=True, null=True)
    emp_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    emp_height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    emp_military = models.CharField(max_length=1, blank=True, null=True)
    emp_citizen_type = models.CharField(max_length=10, blank=True, null=True)
    emp_citizen_id = models.CharField(max_length=13, blank=True, null=True)
    emp_issue_date = models.DateTimeField(blank=True, null=True)
    emp_expiry_date = models.DateTimeField(blank=True, null=True)
    emp_issue_place = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    emp_issue_city = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    emp_issue_country = models.SmallIntegerField(blank=True, null=True)
    emp_type = models.CharField(max_length=2, blank=True, null=True)
    emp_com = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    emp_brn = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    emp_div = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    emp_dept = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    emp_sect = models.SmallIntegerField(blank=True, null=True)
    emp_position = models.SmallIntegerField(blank=True, null=True)
    emp_rank = models.CharField(max_length=3, blank=True, null=True)
    emp_grade = models.SmallIntegerField(blank=True, null=True)
    emp_status = models.SmallIntegerField(blank=True, null=True)
    emp_payid = models.SmallIntegerField(blank=True, null=True)
    salary_active = models.BooleanField(blank=True, null=True)
    emp_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    emp_wage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    emp_template = models.SmallIntegerField(blank=True, null=True)
    emp_join_date = models.DateTimeField(blank=True, null=True)
    emp_term_date = models.DateTimeField(blank=True, null=True)
    emp_work = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    emp_lve_id = models.CharField(max_length=5, blank=True, null=True)
    emp_acc_no = models.CharField(max_length=10, blank=True, null=True)
    emp_acc_type = models.SmallIntegerField(blank=True, null=True)
    emp_acc_bank = models.SmallIntegerField(blank=True, null=True)
    emp_acc_brn = models.CharField(max_length=50, blank=True, null=True)
    emp_acc_city = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    emp_tax = models.CharField(max_length=20, blank=True, null=True)
    emp_last_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    emp_last_wht = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    emp_house = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    emp_insurance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    emp_donation = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    emp_family = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    emp_doc_no = models.CharField(max_length=10, blank=True, null=True)
    sch_active = models.BooleanField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)
    empstatus = models.CharField(db_column='EmpStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emp_wkcountry = models.SmallIntegerField(blank=True, null=True)
    emp_spid = models.CharField(db_column='emp_SpID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    emp_jobfnt = models.CharField(max_length=6, blank=True, null=True)
    emp_cate = models.SmallIntegerField(blank=True, null=True)
    emp_headcount = models.CharField(max_length=5, blank=True, null=True)
    randomno = models.DecimalField(db_column='RandomNo', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    emp_loan = models.DecimalField(db_column='Emp_Loan', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EMPLOYEE'


class Flooring(models.Model):
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=255, blank=True, null=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    image_image_field = models.CharField(db_column='Image (image)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    overview = models.CharField(db_column='Overview', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Flooring'


class LeaveHoliday(models.Model):
    hol_date = models.DateTimeField()
    pub_id = models.SmallIntegerField(blank=True, null=True)
    pub_th = models.CharField(db_column='PUB_TH', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pub_en = models.CharField(db_column='PUB_EN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    upd_date = models.DateTimeField()
    upd_by = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'LEAVE_HOLIDAY'


class LeaveType(models.Model):
    lve_id = models.DecimalField(max_digits=3, decimal_places=0)
    lve_th = models.CharField(max_length=50, blank=True, null=True)
    lve_en = models.CharField(max_length=50, blank=True, null=True)
    lve_code = models.CharField(max_length=3, blank=True, null=True)
    pay_type = models.CharField(max_length=3, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)
    lve_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LEAVE_TYPE'


class LeavePlan(models.Model):
    lve_year = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    emp_id = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    lve_id = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    lve_code = models.CharField(max_length=3, blank=True, null=True)
    lve_plan = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    lve_plan_hr = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    lve_act = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    lve_act_hr = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    lve_miss = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    lve_miss_hr = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    upd_date = models.DateTimeField()
    upd_by = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'Leave_Plan'


class LeaveEmployee(models.Model):
    emp_id = models.DecimalField(max_digits=7, decimal_places=0)
    emp_fname_en = models.CharField(max_length=30, blank=True, null=True)
    emp_lname_en = models.CharField(max_length=40, blank=True, null=True)
    emp_fname_th = models.CharField(max_length=30, blank=True, null=True)
    emp_lname_th = models.CharField(max_length=40, blank=True, null=True)
    pos_th = models.CharField(max_length=50, blank=True, null=True)
    pos_en = models.CharField(max_length=50, blank=True, null=True)
    div_th = models.CharField(max_length=50, blank=True, null=True)
    div_en = models.CharField(max_length=50, blank=True, null=True)
    emp_type = models.CharField(max_length=2, blank=True, null=True)
    emp_join_date = models.DateTimeField(blank=True, null=True)
    emp_term_date = models.DateTimeField(blank=True, null=True)
    upd_date = models.DateTimeField()
    upd_by = models.CharField(max_length=6)
    emp_passcode = models.CharField(db_column='Emp_passcode', max_length=4, blank=True, null=True)  # Field name made lowercase.
    emp_spid = models.DecimalField(db_column='Emp_SpID', max_digits=7, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=13)

    class Meta:
        managed = False
        db_table = 'Leave_employee'


class TclContractQty(models.Model):
    cnt_id = models.CharField(max_length=13, blank=True, null=True)
    cus_name_th = models.CharField(max_length=120, blank=True, null=True)
    zone_en = models.CharField(max_length=30, blank=True, null=True)
    cnt_sign_frm = models.CharField(max_length=30, blank=True, null=True)
    cnt_sign_to = models.CharField(max_length=30, blank=True, null=True)
    cus_add1_th = models.CharField(max_length=150, blank=True, null=True)
    city_th = models.CharField(max_length=30, blank=True, null=True)
    sd = models.DecimalField(db_column='SD', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sn = models.DecimalField(db_column='SN', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    cqty = models.DecimalField(db_column='CQTY', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    dly_sd = models.IntegerField(db_column='DLY_SD')  # Field name made lowercase.
    dly_sn = models.IntegerField(db_column='DLY_SN')  # Field name made lowercase.
    dly_std = models.IntegerField(db_column='DLY_STD')  # Field name made lowercase.
    dly_stn = models.IntegerField(db_column='DLY_STN')  # Field name made lowercase.
    dly_dof = models.IntegerField(db_column='DLY_DOF')  # Field name made lowercase.
    dly_date = models.CharField(db_column='Dly_Date', max_length=13)  # Field name made lowercase.
    upd_date = models.CharField(db_column='UPD_Date', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TCl_Contract_QTY'


class TAprove(models.Model):
    apr_id = models.DecimalField(primary_key=True, max_digits=6, decimal_places=0)
    apr_title = models.SmallIntegerField(blank=True, null=True)
    apr_name_th = models.CharField(max_length=60, blank=True, null=True)
    apr_name_en = models.CharField(max_length=60, blank=True, null=True)
    apr_pos_th = models.CharField(max_length=50, blank=True, null=True)
    apr_pos_en = models.CharField(max_length=50, blank=True, null=True)
    apr_piority = models.CharField(max_length=3)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_APROVE'


class TCity(models.Model):
    city_id = models.DecimalField(primary_key=True, max_digits=2, decimal_places=0)
    country_id = models.SmallIntegerField(blank=True, null=True)
    city_th = models.CharField(max_length=30, blank=True, null=True)
    city_en = models.CharField(max_length=30, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_CITY'


class TCountry(models.Model):
    country_id = models.SmallIntegerField(primary_key=True)
    country_sht = models.CharField(max_length=3, blank=True, null=True)
    country_th = models.CharField(max_length=30, blank=True, null=True)
    country_en = models.CharField(max_length=30, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_COUNTRY'


class TDistrict(models.Model):
    dist_id = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    city_id = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    dist_th = models.CharField(max_length=30, blank=True, null=True)
    dist_en = models.CharField(max_length=30, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_DISTRICT'


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


class TWagezone(models.Model):
    wage_id = models.DecimalField(primary_key=True, max_digits=2, decimal_places=0)
    wage_th = models.CharField(max_length=30, blank=True, null=True)
    wage_en = models.CharField(max_length=30, blank=True, null=True)
    wage_city = models.SmallIntegerField(blank=True, null=True)
    wage_8hr = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    owage_8hr = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    wage_en_tmp = models.CharField(max_length=50, blank=True, null=True)
    w2010 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    w2009 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    w2008 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    w2007 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    w2006 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    w2005 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    w2004 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_WAGEZONE'


class VBiDlyPlanWork(models.Model):
    zone_en = models.CharField(max_length=30, blank=True, null=True)
    qty = models.DecimalField(db_column='Qty', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_BI_DLY_Plan_work'


class VBiFeebyzone(models.Model):
    zone_en = models.CharField(max_length=30, blank=True, null=True)
    fee = models.DecimalField(db_column='Fee', max_digits=38, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_BI_FEEBYZONE'


class VBiTop10(models.Model):
    cus_name_en = models.CharField(max_length=120, blank=True, null=True)
    fee = models.DecimalField(db_column='Fee', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_BI_Top10'


class VContractActive(models.Model):
    cus_id = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    cus_loc = models.CharField(max_length=7, blank=True, null=True)
    cnt_id = models.DecimalField(max_digits=13, decimal_places=0)
    zone_en = models.CharField(max_length=30, blank=True, null=True)
    cus_name_en = models.CharField(max_length=120, blank=True, null=True)
    bgroup = models.CharField(db_column='Bgroup', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cnt_sale_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cnt_doc_no = models.CharField(max_length=25, blank=True, null=True)
    cnt_sign_frm = models.DateTimeField(blank=True, null=True)
    cnt_sign_to = models.DateTimeField(blank=True, null=True)
    cnt_guard_amt = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    cus_taxid = models.CharField(max_length=30, blank=True, null=True)
    btype = models.CharField(db_column='Btype', max_length=100, blank=True, null=True)  # Field name made lowercase.
    btype1 = models.CharField(db_column='Btype1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    btype2 = models.CharField(db_column='Btype2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cnt_eff_frm = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'V_CONTRACT_ACTIVE'


class VContractActiveQty(models.Model):
    cus_id = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    cnt_id = models.DecimalField(max_digits=13, decimal_places=0)
    zone_en = models.CharField(max_length=30, blank=True, null=True)
    cus_name_en = models.CharField(max_length=120, blank=True, null=True)
    cnt_sale_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cnt_doc_no = models.CharField(max_length=25, blank=True, null=True)
    cnt_guard_amt = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    cnt_guard_work = models.DecimalField(db_column='cnt_guard_Work', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    opn1 = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    opn2 = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    op1 = models.CharField(max_length=25, blank=True, null=True)
    op2 = models.CharField(max_length=25, blank=True, null=True)
    cnt_zone = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'V_CONTRACT_ACTIVE_QTY'


class VDlyPlan(models.Model):
    cnt_id = models.DecimalField(max_digits=13, decimal_places=0)
    cnt_guard_amt = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'V_DLY_plan'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Groupbill(models.Model):
    post = models.FloatField(db_column='Post', blank=True, null=True)  # Field name made lowercase.
    cnt_id = models.CharField(db_column='Cnt_id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    groupcom = models.CharField(db_column='GroupCom', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'groupbill'


class LeaveEmployeeNew(models.Model):
    emp_id = models.DecimalField(max_digits=7, decimal_places=0)
    emp_fname_en = models.CharField(max_length=30, blank=True, null=True)
    emp_lname_en = models.CharField(max_length=40, blank=True, null=True)
    emp_fname_th = models.CharField(max_length=30, blank=True, null=True)
    emp_lname_th = models.CharField(max_length=40, blank=True, null=True)
    pos_th = models.CharField(max_length=50, blank=True, null=True)
    pos_en = models.CharField(max_length=50, blank=True, null=True)
    div_th = models.CharField(max_length=50, blank=True, null=True)
    div_en = models.CharField(max_length=50, blank=True, null=True)
    emp_type = models.CharField(max_length=2, blank=True, null=True)
    emp_join_date = models.DateTimeField(blank=True, null=True)
    emp_term_date = models.DateTimeField(blank=True, null=True)
    upd_date = models.DateTimeField()
    upd_by = models.CharField(max_length=6)
    emp_passcode = models.CharField(db_column='Emp_passcode', max_length=4, blank=True, null=True)  # Field name made lowercase.
    emp_spid = models.DecimalField(db_column='Emp_SpID', max_digits=7, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=13)

    class Meta:
        managed = False
        db_table = 'leave_employee_new'


class LeaveEmployeeinstance(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField()
    created_by = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    lve_act = models.IntegerField(blank=True, null=True)
    lve_act_hr = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    status = models.CharField(max_length=1)
    emp_id = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    leave_type_id = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'leave_employeeinstance'


class PageUserprofile(models.Model):
    language_code = models.CharField(max_length=2, blank=True, null=True)
    employee_id = models.CharField(max_length=10, blank=True, null=True)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'page_userprofile'


class PostOfficeAttachment(models.Model):
    file = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=255)
    headers = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_office_attachment'


class PostOfficeAttachmentEmails(models.Model):
    attachment = models.ForeignKey(PostOfficeAttachment, models.DO_NOTHING)
    email = models.ForeignKey('PostOfficeEmail', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'post_office_attachment_emails'


class PostOfficeEmail(models.Model):
    from_email = models.CharField(max_length=254)
    to = models.TextField()
    cc = models.TextField()
    bcc = models.TextField()
    subject = models.CharField(max_length=989)
    message = models.TextField()
    html_message = models.TextField()
    status = models.SmallIntegerField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    created = models.DateTimeField()
    last_updated = models.DateTimeField()
    scheduled_time = models.DateTimeField(blank=True, null=True)
    headers = models.TextField(blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    template = models.ForeignKey('PostOfficeEmailtemplate', models.DO_NOTHING, blank=True, null=True)
    backend_alias = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'post_office_email'


class PostOfficeEmailtemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.CharField(max_length=255)
    content = models.TextField()
    html_content = models.TextField()
    created = models.DateTimeField()
    last_updated = models.DateTimeField()
    default_template = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    language = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'post_office_emailtemplate'
        unique_together = (('name', 'language', 'default_template'),)


class PostOfficeLog(models.Model):
    date = models.DateTimeField()
    status = models.SmallIntegerField()
    exception_type = models.CharField(max_length=255)
    message = models.TextField()
    email = models.ForeignKey(PostOfficeEmail, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'post_office_log'
