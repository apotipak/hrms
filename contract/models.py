from django.db import models
from customer.models import Customer


class CusContract(models.Model):
    cnt_id = models.DecimalField(primary_key=True, max_digits=13, decimal_places=0)
    
    cus_id = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    #cus_id = models.ForeignKey(Customer, db_column='cus_id', to_field='cus_id', on_delete=models.SET_NULL, null=True) 

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
    cnt_wage_id = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
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
        managed = True
        db_table = 'CUS_CONTRACT'