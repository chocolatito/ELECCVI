from .base import *
print(f"{env.str('USER')}:{env.str('PASSWORD')}")
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'eleccvi',
        'USER':  env.str('USER'),
        'PASSWORD': env.str('PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
