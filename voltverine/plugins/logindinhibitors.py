from __future__ import absolute_import
from __future__ import print_function
from .basedbusplugin import BaseDbusPlugin
from .constants import (DUNNO, OK, NOT_OK)
import logging
logger = logging.getLogger(__name__)


class LogindInhibitors(BaseDbusPlugin):

    def analyze(self):
        try:
            logind = self._system_bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
            inhibitors = logind.ListInhibitors(dbus_interface='org.freedesktop.login1.Manager')
            shutdowninhib = list(filter(lambda x: "shutdown" in x[0] and "block" in x[3], inhibitors))

            if len(shutdowninhib):
                return (NOT_OK, {'sessions': len(shutdowninhib)})
            else:
                return (OK, {})
        except:
            return (DUNNO, {})
