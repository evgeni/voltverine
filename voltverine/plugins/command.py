from __future__ import absolute_import
from .baseplugin import BasePlugin
from .constants import (DUNNO, OK, NOT_OK)
import subprocess
import shlex
import logging
logger = logging.getLogger(__name__)


class Command(BasePlugin):

    def __init__(self, command=None, *args, **kwargs):
        super(Command, self).__init__(args, kwargs)
        if isinstance(command, list):
            self._command = command
        elif command:
            self._command = shlex.split(command)
        else:
            self._command = None

    def analyze(self):
        if not self._command:
            return (DUNNO, {})
        try:
            retcode = subprocess.call(self._command)
            if retcode != 0:
                return (NOT_OK, {'retcode': retcode})
            else:
                return (OK, {'retcode': retcode})
        except OSError:
            return (DUNNO, {})
