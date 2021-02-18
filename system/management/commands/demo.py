from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.db import connection


class Command(BaseCommand):
	def handle(self, **options):
				
		TURN_CAR_FORM_SEND_MAIL_ON = getattr(settings, "TURN_CAR_FORM_SEND_MAIL_ON", None)	
		TURN_CAR_FORM_DUMMY_EMAIL_ON = getattr(settings, "TURN_CAR_FORM_DUMMY_EMAIL_ON", None)
		CAR_FORM_DUMMY_EMAIL = getattr(settings, "CAR_FORM_DUMMY_EMAIL", None)

		print("DEMO")
