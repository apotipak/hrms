from django.db import models


class Covid19Report(models.Model):
    class Meta:
        permissions = (
            ("can_access_covid_19_report", "Can access Covid 19 report"),
        )
