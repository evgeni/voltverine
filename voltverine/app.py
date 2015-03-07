import argparse
import inspect
import logging
import os
import sys
import importlib
import yaml
import time
try:
    import daemon
except ImportError:
    daemon = False
import voltverine.plugins
import voltverine.actions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_PLUGIN_BLACKLIST = ['BasePlugin', 'BaseDbusPlugin']
_DEFAULT_CONFIG = {'action': 'LogindPoweroff', 'plugins': []}


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
        if daemon:
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
                _yaml_config = yaml.safe_load(configfile)
                if _yaml_config:
                    self.config.update(_yaml_config)
        _args_config = {
            'daemonize': self.args.daemonize,
            'foreground': self.args.foreground,
            'dry_run': self.args.dry_run,
            'verbose': self.args.verbose,
            'all_plugins': self.args.all_plugins,
            }
        self.config.update(_args_config)

    def _find_plugins(self):
        if self.config['plugins']:
            self._plugins = []
            if isinstance(self.config['plugins'], dict):
                configured_plugins = self.config['plugins'].keys()
            elif isinstance(self.config['plugins'], list):
                configured_plugins = self.config['plugins']
            else:
                configured_plugins = []
            for plugin in configured_plugins:
                if hasattr(voltverine.plugins, plugin):
                    self._plugins.append((plugin, getattr(voltverine.plugins, plugin)))
                elif '.' in plugin:
                    try:
                        mod, cls = plugin.rsplit('.', 1)
                        plugin_module = importlib.import_module(mod)
                        self._plugins.append((plugin, getattr(plugin_module, cls)))
                    except ImportError:
                        logger.error("Could not import configured plugin %s", plugin)
                else:
                    logger.error("Could not find configured plugin %s", plugin)
        else:
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
        if daemon and self.args.daemonize:
            with daemon.DaemonContext():
                self._run_in_loop()
        elif self.args.foreground:
            self._run_in_loop()
        else:
            self._run()

    def _run_in_loop(self):
        while True:
            self._run()
            time.sleep(10)

    def _run(self):
        results = {voltverine.plugins.NOT_OK: 0, voltverine.plugins.OK: 0, voltverine.plugins.DUNNO: 0}
        for plugin in self._plugins:
            logger.debug("Trying %s", plugin[0])
            if (isinstance(self.config['plugins'], dict) and self.config['plugins'].has_key(plugin[0]) and self.config['plugins'][plugin[0]]):
                pobj = plugin[1](**self.config['plugins'][plugin[0]])
            else:
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
