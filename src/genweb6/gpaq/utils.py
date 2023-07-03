# -*- coding: utf-8 -*-
from plone.memoize import ram
from plone.registry.interfaces import IRegistry
from time import time
from zope.component import queryUtility

from genweb6.gpaq.controlpanel.gpaq import IGpaqSettings


@ram.cache(lambda *args: time() // (24 * 60 * 60))
def genwebGpaqConfig():
    registry = queryUtility(IRegistry)
    return registry.forInterface(IGpaqSettings)
