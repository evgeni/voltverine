import argparse
import inspect
import logging
import voltverine.plugins
import voltverine.actions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_PLUGIN_BLACKLIST = ['BasePlugin', 'BaseDbusPlugin']


class VoltverineApp(object):

    def __init__(self):
        self._parse_args()
        if self.args.verbose:
            # get the "root" logger and set it to DEBUG
            logging.getLogger().setLevel(logging.DEBUG)
        self._find_plugins()
        self._action = voltverine.actions.LogindPoweroff()

    def _parse_args(self):
        parser = argparse.ArgumentParser(description='maybe shutdown the machine')
        parser.add_argument('-d', '--daemonize', action='store_true')
        parser.add_argument('-f', '--foreground', action='store_true')
        parser.add_argument('-n', '--dry-run', action='store_true')
        parser.add_argument('-v', '--verbose', action='store_true')
        parser.add_argument('-c', '--config', action='store')
        parser.add_argument('-a', '--all-plugins', action='store_true')
        parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
        self.args = parser.parse_args()

    def _find_plugins(self):
        self._plugins = inspect.getmembers(voltverine.plugins,
                                           lambda x: inspect.isclass(x) and
                                           x.__name__ not in _PLUGIN_BLACKLIST)

    def run(self):
        if self.args.daemonize:
            # do something to run self._run() as a daemon
            pass
        elif self.args.foreground:
            # do something to run self._run() in a loop in foreground
            pass
        else:
            self._run()

    def _run(self):
        results = {voltverine.plugins.NOT_OK: 0, voltverine.plugins.OK: 0, voltverine.plugins.DUNNO: 0}
        for plugin in self._plugins:
            logger.debug("Trying %s", plugin[0])
            pobj = plugin[1]()
            (result, info) = pobj.analyze()
            if result is voltverine.plugins.NOT_OK and not self.args.all_plugins:
                logger.info("%s decided we cannot shutdown now, skipping the other plugins", plugin[0])
                return
            logger.info((result, info))
            results[result] += 1
        if results[voltverine.plugins.NOT_OK] > 0:
            logger.debug("plugins decided not to take action")
        elif results[voltverine.plugins.OK] > 0:
            logger.debug("executing action")
            if not self.args.dry_run:
                self._action.execute()
        else:
            logger.info("nobody said it is ok to execute an action")
