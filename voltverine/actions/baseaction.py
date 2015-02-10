import logging
logger = logging.getLogger(__name__)


class BaseAction(object):

    def __init__(self, *args, **kwargs):
        pass

    def execute(self):
        logger.info("called execute() of BaseAction")
