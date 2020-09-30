from django.db import models
from customer.models import Customer
from system.models import CusContact, TAprove, TWagezone, ComRank, TShift


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
    cnt_apr_by = models.ForeignKey(TAprove, db_column='cnt_apr_by', to_field='apr_id', on_delete=models.SET_NULL, blank=True, null=True)
    cnt_guard_amt = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    cnt_sale_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)    
    cnt_wage_id = models.ForeignKey(TWagezone, related_name='cus_contract_t_wagezone_fk', db_column='cnt_wage_id', to_field='wage_id', on_delete=models.SET_NULL, null=True, blank=True)
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


class CusService(models.Model):
    srv_id = models.DecimalField(primary_key=True, max_digits=16, decimal_places=0)
    # cnt_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    cnt_id = models.ForeignKey(CusContract, db_column='cnt_id', to_field='cnt_id', on_delete=models.SET_NULL, null=True)
    srv_rank = models.CharField(max_length=3, blank=True, null=True)
    
    # srv_shif_id = models.SmallIntegerField(blank=True, null=True)
    srv_shif_id = models.ForeignKey(TShift, db_column='srv_shif_id', to_field='shf_id', on_delete=models.SET_NULL, null=True)

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
