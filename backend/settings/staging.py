
import django_heroku

from backend.settings.common import *

print('ENVIRONMENT = staging - setting debug to true and SECURE_SSL_REDIRECT to True')
DEBUG = True

# heroku settings
django_heroku.settings(locals())

TWILIO_CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
