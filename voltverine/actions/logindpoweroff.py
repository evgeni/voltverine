from .basedbusaction import BaseDbusAction
import logging
logger = logging.getLogger(__name__)


class LogindPoweroff(BaseDbusAction):

    def execute(self):
        try:
            logind = self._system_bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
            logind.PowerOff(False)
        except:
            pass
