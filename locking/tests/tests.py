from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from .factories import LockFactory


class ExpirationTestCase(TestCase):

    def test_lock_seconds_remaining(self):
        lock = LockFactory(_locked_at=timezone.now())
        actual = lock.lock_seconds_remaining
        expected = 120 # must match default in locking.settings
        self.assertAlmostEqual(expected, actual, delta=1)
