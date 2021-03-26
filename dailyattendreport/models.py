from django.db import models

class DailyAttendReport(models.Model):
    class Meta:
        permissions = (
            ("can_access_daily_attend_report", "Can accces Daily Attend report"),
            ("can_access_gpm403_daily_guard_performance_by_contract_report", "Can accces GPM403 Daily Guard Performance by Contract report"),
            ("can_access_gpm_work_on_day_off_report", "Can accces GPM Work on Day Off report"),
        )
