from django.db import models
from system.models import ComZone, TTitle, TDistrict, CusContact, TCity, TCountry


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
    cus_district = models.ForeignKey(TDistrict, db_column='cus_district', to_field='dist_id', on_delete=models.SET_NULL, null=True)    
    cus_city = models.ForeignKey(TCity, db_column='cus_city', to_field='city_id', on_delete=models.SET_NULL, null=True)
    cus_country = models.ForeignKey(TCountry, db_column='cus_country', to_field='country_id', on_delete=models.SET_NULL, null=True)
    cus_zip = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    cus_tel = models.CharField(max_length=40, blank=True, null=True)
    cus_fax = models.CharField(max_length=30, blank=True, null=True)
    cus_email = models.CharField(max_length=60, blank=True, null=True)
    cus_taxid = models.CharField(max_length=30, blank=True, null=True)
    cus_active = models.BooleanField(blank=True, null=True)
    cus_bill = models.BooleanField(blank=True, null=True)
    cus_main = models.BooleanField(blank=True, null=True)
    cus_site = models.BooleanField(blank=True, null=True)
    cus_zone = models.ForeignKey(ComZone, db_column='cus_zone', to_field='zone_id', on_delete=models.SET_NULL, null=True) 
    
    cus_contact = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    # cus_contact = models.ForeignKey(CusContact, db_column='cus_contact', to_field='con_id', on_delete=models.SET_NULL, null=True)

    site_contact = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    last_contact = models.SmallIntegerField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    upd_by = models.CharField(max_length=10, blank=True, null=True)
    upd_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'CUSTOMER'
        ordering = ['cus_no']

