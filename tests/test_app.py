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
        sys.argv = ['voltverine']
        v = voltverine.app.VoltverineApp()
        output = sys.stdout.getvalue().strip() # because stdout is an StringIO instance
        self.assertEquals(output, '')
        self.assertTrue(v._plugins)
        self.assertTrue(v._action.__class__.__name__ == 'LogindPoweroff')

    def test_help(self):
        with self.assertRaises(SystemExit) as cm:
            sys.argv = ['voltverine', '-h']
            v = voltverine.app.VoltverineApp()
        output = sys.stdout.getvalue().strip() # because stdout is an StringIO instance
        self.assertRegex(output, 'usage')
        self.assertRegex(output, 'voltverine')
        self.assertEquals(cm.exception.code, 0)

    def test_config_plugins_dict(self):
        with tempfile.NamedTemporaryFile() as cfgf:
            cfgf.write("""---
plugins:
  NoShutdownFile:
    filename: /some/path
""")
            cfgf.flush()
            sys.argv = ['voltverine', '-c', cfgf.name]
            v = voltverine.app.VoltverineApp()
            self.assertEquals(len(v._plugins), 1)
            self.assertEquals(v._plugins[0][0], 'NoShutdownFile')
            self.assertEquals(v.config['plugins']['NoShutdownFile']['filename'], '/some/path')

    def test_config_plugins_list(self):
        with tempfile.NamedTemporaryFile() as cfgf:
            cfgf.write("""---
plugins:
  - LogindSessions
  - LogindInhibitors
""")
            cfgf.flush()
            sys.argv = ['voltverine', '-c', cfgf.name]
            v = voltverine.app.VoltverineApp()
            self.assertEquals(len(v._plugins), 2)
            self.assertTrue('LogindSessions' in v.config['plugins'])
            self.assertTrue('LogindInhibitors' in v.config['plugins'])

if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
