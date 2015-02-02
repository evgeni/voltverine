from __future__ import absolute_import
from .baseplugin import BasePlugin
import dbus
import logging
logger = logging.getLogger(__name__)


class BaseDbusPlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        super(BaseDbusPlugin, self).__init__(args, kwargs)
        self._system_bus = dbus.SystemBus()
