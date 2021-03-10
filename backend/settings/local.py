
import dj_database_url


from backend.settings.common import *


print('ENVIRONMENT = local - setting debug to true')
DEBUG = True

# databases
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=False)

ssl._create_default_https_context = ssl._create_unverified_context

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
