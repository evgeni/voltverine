from __future__ import absolute_import
from .baseplugin import BasePlugin
from .constants import (DUNNO, OK, NOT_OK)
import logging
logger = logging.getLogger(__name__)


class Uptime(BasePlugin):

    def __init__(self, uptime=60, *args, **kwargs):
        super(Uptime, self).__init__(args, kwargs)
        self._uptime = uptime * 60

    def analyze(self):
        with open('/proc/uptime') as uptime:
            l = uptime.read()
            seconds = float(l.split()[0])
            if seconds > self._uptime:
                return (OK, {'uptime': seconds})
            else:
                return (NOT_OK, {'uptime': seconds})
