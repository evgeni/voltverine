from .baseaction import BaseAction
import dbus
import logging
logger = logging.getLogger(__name__)


class BaseDbusAction(BaseAction):

    def __init__(self, *args, **kwargs):
        super(BaseDbusAction, self).__init__(args, kwargs)
        self._system_bus = dbus.SystemBus()
