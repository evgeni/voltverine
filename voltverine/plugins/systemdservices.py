from __future__ import absolute_import
from .basedbusplugin import BaseDbusPlugin
from .constants import (DUNNO, OK, NOT_OK)
import logging
logger = logging.getLogger(__name__)


class SystemdServices(BaseDbusPlugin):

    def __init__(self, services=[], *args, **kwargs):
        super(SystemdServices, self).__init__(args, kwargs)
        self._services = services

    def analyze(self):
        try:
            systemd = self._system_bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
            units = systemd.ListUnits(dbus_interface='org.freedesktop.systemd1.Manager')
            running = list(filter(lambda x: ".service" in x[0] and "running" in x[4], units))

            services = []
            for service in running:
                if service[0][0:-8] in self._services:
                    services.append(service)

            if len(services):
                return (NOT_OK, {'services': len(services)})
            else:
                return (OK, {})
        except:
            return (DUNNO, {})
