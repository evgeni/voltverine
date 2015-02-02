from __future__ import absolute_import
from .constants import (DUNNO, OK, NOT_OK)
import logging
logger = logging.getLogger(__name__)


class BasePlugin(object):

    def __init__(self, *args, **kwargs):
        pass

    def analyze(self):
        return (DUNNO, {})
