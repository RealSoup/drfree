from .base import *

ALLOWED_HOSTS = ['13.125.137.210', 'bbangdorf.kro.kr']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'drfree',
        'USER': 'drfree',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',   # or your RDS/EC2 IP
        'PORT': '3306',
    }
}