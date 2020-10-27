from django.db import models


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


class DlyPlanHis(models.Model):
    trans_date = models.DateTimeField()
    cnt_id = models.DecimalField(max_digits=13, decimal_places=0)
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
        db_table = 'DLY_PLAN_HIS'


class SchPlan(models.Model):
    sch_no = models.DecimalField(primary_key=True, max_digits=20, decimal_places=0)
    srv_id = models.DecimalField(max_digits=16, decimal_places=0, blank=True, null=True)
    cnt_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    emp_id = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    sch_rank = models.CharField(max_length=3, blank=True, null=True)
    relief = models.BooleanField(blank=True, null=True)
    sch_date_frm = models.DateTimeField(blank=True, null=True)
    sch_date_to = models.DateTimeField(blank=True, null=True)
    sch_shf_mon = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    sch_shf_tue = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    sch_shf_wed = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    sch_shf_thu = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    sch_shf_fri = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    sch_shf_sat = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    sch_shf_sun = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    sch_active = models.BooleanField(blank=False, null=False)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SCH_PLAN'

