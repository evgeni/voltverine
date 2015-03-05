from __future__ import absolute_import
from .baseplugin import BasePlugin
from .constants import (DUNNO, OK, NOT_OK)
import datetime
import logging
logger = logging.getLogger(__name__)


class Time(BasePlugin):

    def __init__(self, time=None, *args, **kwargs):
        super(Time, self).__init__(args, kwargs)
        self._times = []
        if time:
            if not isinstance(time, list):
                time = [time]
            for t in time:
                try:
                    start = datetime.datetime.strptime(t['start'], '%H:%M').time()
                    end = datetime.datetime.strptime(t['end'], '%H:%M').time()
                    self._times.append({'start': start, 'end': end})
                except ValueError:
                    logger.warn("Could not parse %s" % t)

    def analyze(self):
        if not self._times:
            return (DUNNO, {})
        now = datetime.datetime.now().time()
        for t in self._times:
            if t['start'] <= now <= t['end']:
                return (NOT_OK, {})
        return (OK, {})
