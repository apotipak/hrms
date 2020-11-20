from django.db import models
from system.models import TEmpsts


class Employee(models.Model):
    emp_id = models.DecimalField(primary_key=True, max_digits=7, decimal_places=0)
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
    
    # emp_status = models.SmallIntegerField(blank=True, null=True)
    emp_status = models.ForeignKey(TEmpsts, related_name='employee_t_empsts_fk_1', db_column='emp_status', to_field='sts_id', on_delete=models.SET_NULL, null=True)

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

class EmpPhoto(models.Model):
    emp_id = models.DecimalField(primary_key=True, max_digits=7, decimal_places=0)
    image_title = models.CharField(max_length=100, blank=True, null=True)
    image_path = models.CharField(max_length=100, blank=True, null=True)
    image = models.BinaryField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EMP_PHOTO'
