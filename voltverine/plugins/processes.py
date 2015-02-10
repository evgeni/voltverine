from __future__ import absolute_import
from .baseplugin import BasePlugin
from .constants import (DUNNO, OK, NOT_OK)
import logging
import psutil
logger = logging.getLogger(__name__)


class Processes(BasePlugin):

    def __init__(self, processes=[], *args, **kwargs):
        super(Processes, self).__init__(args, kwargs)
        self._processes = processes

    def analyze(self):
        try:
            tmp_processes = []
            for process in psutil.process_iter():
                if process.name() in self._processes:
                    tmp_processes.append(process)

            if len(tmp_processes):
                return (NOT_OK, {'running_processes': len(tmp_processes)})
            else:
                return (OK, {})
        except:
            return (DUNNO, {})
