from __future__ import absolute_import
from .baseplugin import BasePlugin
from .constants import (DUNNO, OK, NOT_OK)
import logging
import psutil
logger = logging.getLogger(__name__)


class ProcessesWithConnections(BasePlugin):

    def __init__(self, processes=[], *args, **kwargs):
        super(ProcessesWithConnections, self).__init__(args, kwargs)
        self._processes = processes

    def analyze(self):
        try:
            running = []
            for process in psutil.process_iter():
                if process.name() in self._processes:
                    running.append(process.pid)

            connections = []
            for conn in psutil.net_connections():
                if conn.pid in running:
                    connections.append(conn)

            if len(connections):
                return (NOT_OK, {'connections': len(connections)})
            else:
                return (OK, {})
        except:
            return (DUNNO, {})
