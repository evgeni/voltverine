from .baseaction import BaseAction
import os
import dbus
import logging
logger = logging.getLogger(__name__)


class BaseDbusAction(BaseAction):

    def __init__(self, *args, **kwargs):
        super(BaseDbusAction, self).__init__(args, kwargs)
        if os.environ.get('DBUS_SYSTEM_BUS_ADDRESS'):
            self._system_bus = dbus.bus.BusConnection(os.environ['DBUS_SYSTEM_BUS_ADDRESS'])
        else:
            self._system_bus = dbus.SystemBus()
