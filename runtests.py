import os.path
import subprocess
import sys

import django
from django.conf import settings

settings.configure(
    DEBUG=True,
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'locking',
    ],
    SECRET_KEY='empty',
    LOCKING={
        'time_until_expiration': 120,
        'time_until_warning': 60
    },
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test',
        },
    },
)

if hasattr(django, 'setup'):
    django.setup()

from django.test.runner import DiscoverRunner
test_runner = DiscoverRunner(verbosity=1, failfast=False)
failures = test_runner.run_tests(['locking', ])
if failures: #pragma no cover
    sys.exit(failures)
