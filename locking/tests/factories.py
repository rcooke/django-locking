#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://factoryboy.readthedocs.io/en/latest/
# pip install factory_boy
import factory

from .. import models

class LockFactory(factory.Factory):
    class Meta:
        model = models.Lock
