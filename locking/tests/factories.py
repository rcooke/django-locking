import factory

from .. import models

class LockFactory(factory.Factory):
    class Meta:
        model = models.Lock
