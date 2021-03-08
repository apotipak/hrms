from django.db import models

class CustomerReport(models.Model):
    class Meta:
        permissions = (
            ("can_access_export_customer_address_main_report", "Can accces Export Customer Address (Main) report"),
        )
