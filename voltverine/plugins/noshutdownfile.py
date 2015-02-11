from __future__ import absolute_import
from .baseplugin import BasePlugin
from .constants import (DUNNO, OK, NOT_OK)
import os
import logging
logger = logging.getLogger(__name__)


class NoShutdownFile(BasePlugin):

    def __init__(self, filename=None, *args, **kwargs):
        super(NoShutdownFile, self).__init__(args, kwargs)
        self._filename = filename

    def analyze(self):
        if not self._filename:
            return (DUNNO, {})
        if os.path.exists(self._filename):
            return (NOT_OK, {})
        else:
            return (OK, {})
