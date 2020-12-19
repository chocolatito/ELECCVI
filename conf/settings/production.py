from .base import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'eleccionvirtual',
        'USER': env.str('USER'),
        'PASSWORD': env.str('PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
