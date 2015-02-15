import argparse
import inspect
import logging
import os
import sys
import yaml
import voltverine.plugins
import voltverine.actions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_PLUGIN_BLACKLIST = ['BasePlugin', 'BaseDbusPlugin']
_DEFAULT_CONFIG = {'action': 'LogindPoweroff'}


class VoltverineApp(object):

    def __init__(self):
        self._parse_args()
        if self.args.verbose:
            # get the "root" logger and set it to DEBUG
            logging.getLogger().setLevel(logging.DEBUG)
        self._parse_config()
        self._find_plugins()
        self._find_action()

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

    def _parse_config(self):
        self.config = _DEFAULT_CONFIG
        if not self.args.config:
            for f in ['voltverine.conf', os.path.expanduser('~/.config/voltverine/voltverine.conf'), '/etc/voltverine/voltverine.conf']:
                if os.path.isfile(f) and os.access(f, os.R_OK):
                    self.args.config = f
                    break
        elif not (os.path.isfile(self.args.config) and os.access(self.args.config, os.R_OK)):
            logger.error("The configuration file is not readable, exiting.")
            sys.exit(1)
        if self.args.config:
            with open(self.args.config) as configfile:
                self.config.update(yaml.safe_load(configfile))
        _args_config = {
            'daemonize': self.args.daemonize,
            'foreground': self.args.foreground,
            'dry_run': self.args.dry_run,
            'verbose': self.args.verbose,
            'all_plugins': self.args.all_plugins,
            }
        self.config.update(_args_config)

    def _find_plugins(self):
        self._plugins = inspect.getmembers(voltverine.plugins,
                                           lambda x: inspect.isclass(x) and
                                           x.__name__ not in _PLUGIN_BLACKLIST)

    def _find_action(self):
        if hasattr(voltverine.actions, self.config['action']):
            self._action = getattr(voltverine.actions, self.config['action'])()
        else:
            logger.error("Could not find defined action %s, exiting", self.config['action'])
            sys.exit(1)

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
