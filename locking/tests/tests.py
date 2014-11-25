from locking.factories import LockFactory
from django.conf import settings
from datetime import datetime
from django.test import TestCase

class ExpirationTestCase(TestCase):

    def test_foo(self):
        lock = LockFactory(_locked_at=datetime.now())
        settings.LOCKING['time_until_expiration'] = 100
        actual = lock.lock_seconds_remaining
        expected = 100
        # allow for the time it's taking the test to run:
        self.assertAlmostEqual(expected, actual, delta=1)
