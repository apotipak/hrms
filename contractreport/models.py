from django.db import models

class ContractReport(models.Model):
    class Meta:
        permissions = (
            ("can_access_contract_menu_report", "Can accces Contract Menu report"),
            ("can_access_contract_list_report", "Can accces Contract List report"),
        )
