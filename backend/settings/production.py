import dj_database_url

import django_heroku

from backend.settings.common import *

print('ENVIRONMENT = production - setting debug to false and SECURE_SSL_REDIRECT to True')
# DEBUG = False
DEBUG = True


# heroku settings
django_heroku.settings(locals())

# print(locals()['DATABASES']['default'])

locals()['DATABASES']['default'] = dj_database_url.config(conn_max_age=django_heroku.MAX_CONN_AGE, ssl_require=True)
