from django.db import models


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
        managed = True
        db_table = 'T_TITLE'

    def __str__(self):
        return self.title_th


class TNation(models.Model):
    nation_id = models.SmallIntegerField(primary_key=True)
    nation_th = models.CharField(max_length=30, blank=True, null=True)
    nation_en = models.CharField(max_length=30, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_NATION'

class ComZone(models.Model):
    zone_id = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    zone_th = models.CharField(max_length=30, blank=True, null=True)
    zone_en = models.CharField(max_length=30, blank=True, null=True)
    zone_emp_id = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'COM_ZONE'

    def __str__(self):
        return '%s - %s' % (self.zone_id,self.zone_en)

class TCountry(models.Model):
    country_id = models.SmallIntegerField(primary_key=True)
    country_sht = models.CharField(max_length=3, blank=True, null=True)
    country_th = models.CharField(max_length=30, blank=True, null=True)
    country_en = models.CharField(max_length=30, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'T_COUNTRY'

    def __str__(self):
        return '%s' % (self.country_th)


class TCity(models.Model):
    city_id = models.DecimalField(primary_key=True, max_digits=2, decimal_places=0)
    
    # country_id = models.SmallIntegerField(blank=True, null=True)
    country_id = models.ForeignKey(TCountry, related_name='tcity_tcountry', db_column='country_id', to_field='country_id', on_delete=models.SET_NULL, null=True)

    city_th = models.CharField(max_length=30, blank=True, null=True)
    city_en = models.CharField(max_length=30, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'T_CITY'

    def __str__(self):
        return self.city_th


class TDistrict(models.Model):
    dist_id = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    
    # city_id = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    city_id = models.ForeignKey(TCity, related_name='tdistrict_tcity', db_column='city_id', to_field='city_id', on_delete=models.SET_NULL, null=True)

    dist_th = models.CharField(max_length=30, blank=True, null=True)
    dist_en = models.CharField(max_length=30, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'T_DISTRICT'

    def __str__(self):
        if self.dist_th:            
            return self.dist_th
        else:
            return ""


class TAprove(models.Model):
    apr_id = models.DecimalField(primary_key=True, max_digits=6, decimal_places=0)
    apr_title = models.ForeignKey(TTitle, db_column='apr_title', to_field='title_id', on_delete=models.SET_NULL, null=True) 
    apr_name_th = models.CharField(max_length=60, blank=True, null=True)
    apr_name_en = models.CharField(max_length=60, blank=True, null=True)
    apr_pos_th = models.CharField(max_length=50, blank=True, null=True)
    apr_pos_en = models.CharField(max_length=50, blank=True, null=True)    
    APPROVE_TYPE = (
        ('', '----------'),
        ('ALL', 'ALL - Can approve all system'),
        ('PRM', 'PRM - Can approve customer performance system'),
        ('PSN', 'PSN - Can approve personel system')        
    )
    #apr_piority = models.CharField(max_length=3, blank=True, null=True)
    apr_piority = models.CharField(
        max_length=3,
        choices=APPROVE_TYPE,
        blank=False,
        null=False,
        default=None)
    upd_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'T_APROVE'

    def __str__(self):
        return self.apr_name_th



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


class CusContact(models.Model):
    con_id = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    # cus_id = models.DecimalField(max_digits=7, unique=True, decimal_places=0)
    cus_id = models.DecimalField(max_digits=7, decimal_places=0)
    cus_brn = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    cus_rem = models.CharField(max_length=10, blank=True, null=True)
    con_type = models.CharField(max_length=1, blank=True, null=True)    
    con_title = models.ForeignKey(TTitle, db_column='con_title', to_field='title_id', on_delete=models.SET_NULL, null=True)    
    con_fname_th = models.CharField(max_length=70, blank=True, null=True)
    con_lname_th = models.CharField(max_length=40, blank=True, null=True)
    con_position_th = models.CharField(max_length=80, blank=True, null=True)
    con_fname_en = models.CharField(max_length=70, blank=True, null=True)
    con_lname_en = models.CharField(max_length=40, blank=True, null=True)
    con_position_en = models.CharField(max_length=80, blank=True, null=True)

    # con_nation = models.SmallIntegerField(blank=True, null=True)
    con_nation = models.ForeignKey(TNation, db_column='con_nation', to_field='nation_id', on_delete=models.SET_NULL, null=True)

    con_sex = models.CharField(max_length=1, blank=True, null=True)
    con_mobile = models.CharField(max_length=30, blank=True, null=True)
    con_email = models.CharField(max_length=70, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'CUS_CONTACT'
        indexes = [
            models.Index(fields=['con_id']),
        ]   

    def __str__(self):
        return '%s %s %s' % (self.con_title, self.con_fname_th, self.con_lname_th)


class Groupbill(models.Model):
    post = models.FloatField(db_column='Post', blank=True, null=True)  # Field name made lowercase.
    cnt_id = models.CharField(db_column='Cnt_id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    groupcom = models.CharField(db_column='GroupCom', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'groupbill'


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
        managed = True
        db_table = 'T_WAGEZONE'


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
        managed = True
        db_table = 'CUS_GROUP'


class HrmsNewLog(models.Model):
    log_table = models.CharField(db_column='log_table', max_length=50, blank=True, null=True)  # Field name made lowercase.
    log_key = models.CharField(db_column='log_key', max_length=50, blank=True, null=True)  # Field name made lowercase.
    log_field = models.CharField(db_column='log_field', max_length=50, blank=True, null=True)  # Field name made lowercase.
    old_value = models.CharField(db_column='old_value', max_length=500, blank=True, null=True)  # Field name made lowercase.
    new_value = models.CharField(db_column='new_value', max_length=500, blank=True, null=True)  # Field name made lowercase.
    log_type = models.CharField(db_column='log_type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    log_by = models.CharField(db_column='log_by', max_length=20, blank=True, null=True)  # Field name made lowercase.
    log_date = models.DateTimeField(db_column='log_date', auto_now_add=True)  # Field name made lowercase.    
    log_description = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'hrms_new_log'
        unique_together = (('id', 'log_date'),)


class TShift(models.Model):
    shf_id = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    shf_type = models.CharField(max_length=1, blank=True, null=True)
    shf_desc = models.CharField(max_length=30, blank=True, null=True)
    shf_time_frm = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    shf_time_to = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    shf_amt_hr = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shf_order = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_SHIFT'


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

class TEmpsts(models.Model):
    sts_id = models.SmallIntegerField(primary_key=True)
    sts_th = models.CharField(max_length=50, blank=True, null=True)
    sts_en = models.CharField(max_length=30, blank=True, null=True)
    sts_flag = models.BooleanField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_EMPSTS'

class TPeriod(models.Model):
    prd_id = models.CharField(primary_key=True, max_length=7)
    prd_year = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    prd_month = models.SmallIntegerField(blank=True, null=True)
    period = models.SmallIntegerField(blank=True, null=True)
    prd_order = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    prd_num = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    prd_date_frm = models.DateTimeField(blank=True, null=True)
    prd_date_to = models.DateTimeField(blank=True, null=True)
    prd_date_paid = models.DateTimeField(blank=True, null=True)
    emp_type = models.CharField(max_length=2, blank=True, null=True)
    com_id = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    prd_close = models.BooleanField(blank=True, null=True)
    prd_process = models.BooleanField(blank=True, null=True)
    prd_wrkday = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_PERIOD'
