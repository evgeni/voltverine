import unittest
import sys
import dbusmock
import subprocess
import tempfile

import voltverine.app

class TestApp(dbusmock.DBusTestCase):

    @classmethod
    def setUpClass(klass):
        klass.start_system_bus()
        klass.dbus_con = klass.get_dbus(True)

    def setUp(self):
        self.p_mock = None
 
    def tearDown(self):
        if self.p_mock:
            self.p_mock.terminate()
            self.p_mock.wait()

    def test_app(self):
        (self.p_mock, obj_logind) = self.spawn_server_template('logind', {}, stdout=subprocess.PIPE)
        sys.argv = ['voltverine']
        v = voltverine.app.VoltverineApp()
        output = sys.stdout.getvalue().strip() # because stdout is an StringIO instance
        self.assertEquals(output, '')
        self.assertTrue(v._plugins)
        self.assertTrue(v._action.__class__.__name__ == 'LogindPoweroff')

    def test_run(self):
        (self.p_mock, obj_logind) = self.spawn_server_template('logind', {}, stdout=subprocess.PIPE)
        sys.argv = ['voltverine']
        v = voltverine.app.VoltverineApp()
        v.run()

    def test_verbose(self):
        (self.p_mock, obj_logind) = self.spawn_server_template('logind', {}, stdout=subprocess.PIPE)
        sys.argv = ['voltverine', '-v']
        v = voltverine.app.VoltverineApp()
        self.assertTrue(v.args.verbose)

    def test_help(self):
        (self.p_mock, obj_logind) = self.spawn_server_template('logind', {}, stdout=subprocess.PIPE)
        with self.assertRaises(SystemExit) as cm:
            sys.argv = ['voltverine', '-h']
            v = voltverine.app.VoltverineApp()
        output = sys.stdout.getvalue().strip() # because stdout is an StringIO instance
        self.assertRegex(output, 'usage')
        self.assertRegex(output, 'voltverine')
        self.assertEquals(cm.exception.code, 0)

    def test_config_plugins_dict(self):
        (self.p_mock, obj_logind) = self.spawn_server_template('logind', {}, stdout=subprocess.PIPE)
        with tempfile.NamedTemporaryFile() as cfgf:
            cfgf.write(b"""---
plugins:
  NoShutdownFile:
    filename: /some/path
""")
            cfgf.flush()
            sys.argv = ['voltverine', '-c', cfgf.name]
            v = voltverine.app.VoltverineApp()
            v.run()
            self.assertEquals(len(v._plugins), 1)
            self.assertEquals(v._plugins[0][0], 'NoShutdownFile')
            self.assertEquals(v.config['plugins']['NoShutdownFile']['filename'], '/some/path')

    def test_config_plugins_list(self):
        (self.p_mock, obj_logind) = self.spawn_server_template('logind', {}, stdout=subprocess.PIPE)
        with tempfile.NamedTemporaryFile() as cfgf:
            cfgf.write(b"""---
plugins:
  - LogindSessions
  - LogindInhibitors
""")
            cfgf.flush()
            sys.argv = ['voltverine', '-c', cfgf.name]
            v = voltverine.app.VoltverineApp()
            v.run()
            self.assertEquals(len(v._plugins), 2)
            self.assertTrue('LogindSessions' in v.config['plugins'])
            self.assertTrue('LogindInhibitors' in v.config['plugins'])

    def test_config_custom_plugins(self):
        (self.p_mock, obj_logind) = self.spawn_server_template('logind', {}, stdout=subprocess.PIPE)
        with tempfile.NamedTemporaryFile() as cfgf:
            cfgf.write(b"""---
plugins:
  - tests.customplugin.CustomPlugin
""")
            cfgf.flush()
            sys.argv = ['voltverine', '-c', cfgf.name]
            v = voltverine.app.VoltverineApp()
            v.run()
            self.assertEquals(len(v._plugins), 1)
            self.assertTrue('tests.customplugin.CustomPlugin' in v.config['plugins'])
            self.assertEquals(v._plugins[0][1].__name__, 'CustomPlugin')

if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
