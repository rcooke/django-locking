INSTALLED_APPS=[
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'locking',
]
SECRET_KEY='empty'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test',
    },
}
