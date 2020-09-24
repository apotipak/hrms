from django.db import models
from system.models import ComZone, TTitle, TDistrict, TCity, TCountry, CusContact, ComZone
# from system.models import ComZone, TTitle, TDistrict, TCity, TCountry, ComZone

class CusMain(models.Model):
    cus_id = models.DecimalField(primary_key=True, max_digits=7, decimal_places=0)    
    cus_sht_th = models.CharField (max_length=10, blank=True, null=True)
    cus_name_th = models.CharField(max_length=120, blank=True, null=True)
    cus_add1_th = models.CharField(max_length=150, blank=True, null=True)
    cus_add2_th = models.CharField(max_length=70, blank=True, null=True)
    cus_subdist_th = models.CharField(max_length=50, blank=True, null=True)
    cus_sht_en = models.CharField(max_length=10, blank=True, null=True)
    cus_name_en = models.CharField(max_length=120, blank=True, null=True)
    cus_add1_en = models.CharField(max_length=150, blank=True, null=True)
    cus_add2_en = models.CharField(max_length=70, blank=True, null=True)
    cus_subdist_en = models.CharField(max_length=50, blank=True, null=True)

    cus_district = models.ForeignKey(TDistrict, related_name='cus_main_t_district_fk', db_column='cus_district', to_field='dist_id', on_delete=models.SET_NULL, null=True)    
    cus_city = models.ForeignKey(TCity, related_name='cus_main_t_city_fk', db_column='cus_city', to_field='city_id', on_delete=models.SET_NULL, null=True)    
    cus_country = models.ForeignKey(TCountry, related_name='cus_main_t_country_fk', db_column='cus_country', to_field='country_id', on_delete=models.SET_NULL, null=True)

    cus_zip = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    cus_tel = models.CharField(max_length=40, blank=True, null=True)
    cus_fax = models.CharField(max_length=30, blank=True, null=True)
    cus_email = models.CharField(max_length=60, blank=True, null=True)
    cus_taxid = models.CharField(max_length=30, blank=True, null=True)
    cus_active = models.BooleanField(blank=True, null=True)
    cus_bill = models.BooleanField(blank=True, null=True)
    cus_main = models.BooleanField(blank=True, null=True)
    cus_site = models.BooleanField(blank=True, null=True)    
    cus_zone = models.ForeignKey(ComZone, related_name='cus_main_com_zone_fk', db_column='cus_zone', to_field='zone_id', on_delete=models.SET_NULL, null=True)
    
    cus_contact = models.ForeignKey(CusContact, related_name='cus_main_cus_contact_fk', db_column='cus_contact', to_field='con_id', on_delete=models.SET_NULL, null=True)
    site_contact = models.ForeignKey(CusContact, related_name='cus_main_site_contact_fk', db_column='site_contact', to_field='con_id', on_delete=models.SET_NULL, null=True)

    last_contact = models.SmallIntegerField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CUS_MAIN'

class CusBill(models.Model):
    cus_no = models.DecimalField(db_column='cus_no', max_digits=10, decimal_places=0,primary_key=True)
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

    cus_district = models.ForeignKey(TDistrict, related_name='cus_bill_t_district_fk', db_column='cus_district', to_field='dist_id', on_delete=models.SET_NULL, null=True)    

    # cus_city = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    cus_city = models.ForeignKey(TCity, related_name='cus_bill_t_city_fk', db_column='cus_city', to_field='city_id', on_delete=models.SET_NULL, null=True)    

    cus_country = models.ForeignKey(TCountry, related_name='cus_bill_t_country_fk', db_column='cus_country', to_field='country_id', on_delete=models.SET_NULL, null=True)

    cus_zip = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    cus_tel = models.CharField(max_length=40, blank=True, null=True)
    cus_fax = models.CharField(max_length=30, blank=True, null=True)
    cus_email = models.CharField(max_length=50, blank=True, null=True)
    cus_taxid = models.CharField(max_length=30, blank=True, null=True)
    cus_active = models.BooleanField(blank=True, null=True)
    cus_bill = models.BooleanField(blank=True, null=True)
    cus_main = models.BooleanField(blank=True, null=True)
    cus_site = models.BooleanField(blank=True, null=True)

    # cus_zone = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    cus_zone = models.ForeignKey(ComZone, related_name='cus_bill_cus_com_zone_fk', db_column='cus_zone', to_field='zone_id', on_delete=models.SET_NULL, null=True)

    # cus_contact = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)    
    # site_contact = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    cus_contact = models.ForeignKey(CusContact, related_name='cus_bill_cus_contact_fk', db_column='cus_contact', to_field='con_id', on_delete=models.SET_NULL, null=True)
    site_contact = models.ForeignKey(CusContact, related_name='cus_bill_site_contact_fk', db_column='site_contact', to_field='con_id', on_delete=models.SET_NULL, null=True)

    last_contact = models.SmallIntegerField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CUS_BILL'


class Customer(models.Model):
    cus_no = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
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

    cus_district = models.ForeignKey(TDistrict, related_name='cus_site_t_district_fk', db_column='cus_district', to_field='dist_id', on_delete=models.SET_NULL, null=True)    
    cus_city = models.ForeignKey(TCity, related_name='cus_site_cus_city_fk', db_column='cus_city', to_field='city_id', on_delete=models.SET_NULL, null=True)
    cus_country = models.ForeignKey(TCountry, related_name='cus_site_t_country_fk', db_column='cus_country', to_field='country_id', on_delete=models.SET_NULL, null=True)

    cus_zip = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    cus_tel = models.CharField(max_length=40, blank=True, null=True)
    cus_fax = models.CharField(max_length=30, blank=True, null=True)
    cus_email = models.CharField(max_length=60, blank=True, null=True)
    cus_taxid = models.CharField(max_length=30, blank=True, null=True)
    cus_active = models.BooleanField(blank=True, null=True)
    cus_bill = models.BooleanField(blank=True, null=True)    
    cus_main = models.BooleanField(blank=True, null=True)
    cus_site = models.BooleanField(blank=True, null=True)
    cus_zone = models.ForeignKey(ComZone, related_name='cus_site_com_zone_fk', db_column='cus_zone', to_field='zone_id', on_delete=models.SET_NULL, null=True)
    
    cus_contact = models.ForeignKey(CusContact, related_name='cus_site_cus_contact_fk', db_column='cus_contact', to_field='con_id', on_delete=models.SET_NULL, null=True)
    site_contact = models.ForeignKey(CusContact, related_name='cus_site_site_contact_fk', db_column='site_contact', to_field='con_id', on_delete=models.SET_NULL, null=True)

    last_contact = models.SmallIntegerField(blank=True, null=True)    
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CUSTOMER'
        ordering = ['cus_no']


class CustomerOption(models.Model):
    cus_no = models.DecimalField(primary_key=True, db_column='CUS_NO', max_digits=10, decimal_places=0)  # Field name made lowercase.
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
