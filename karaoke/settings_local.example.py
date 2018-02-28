# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'extra secret'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your-db-here',
        'USER': 'your-user-here',
        'PASSWORD': 'your-pw-here',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
