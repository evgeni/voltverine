from __future__ import absolute_import
from .basedbusplugin import BaseDbusPlugin
from .constants import (DUNNO, OK, NOT_OK)
import logging
logger = logging.getLogger(__name__)


class LogindSessions(BaseDbusPlugin):

    def analyze(self):
        try:
            logind = self._system_bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
            sessions = logind.ListSessions(dbus_interface='org.freedesktop.login1.Manager')

            if len(sessions):
                return (NOT_OK, {'sessions': len(sessions)})
            else:
                return (OK, {})
        except:
            return (DUNNO, {})
