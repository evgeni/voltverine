from __future__ import absolute_import
from .baseplugin import BasePlugin
import os
import dbus
import logging
logger = logging.getLogger(__name__)


class BaseDbusPlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        super(BaseDbusPlugin, self).__init__(args, kwargs)
        if os.environ.get('DBUS_SYSTEM_BUS_ADDRESS'):
            self._system_bus = dbus.bus.BusConnection(os.environ['DBUS_SYSTEM_BUS_ADDRESS'])
        else:
            self._system_bus = dbus.SystemBus()
