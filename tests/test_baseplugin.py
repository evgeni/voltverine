import unittest
import sys
import dbusmock
import subprocess

import voltverine.plugins

class TestBasePlugin(dbusmock.DBusTestCase):

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

    def test_baseplugin(self):
        voltverine_plugin = voltverine.plugins.BasePlugin()
        (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.DUNNO)
        self.assertTrue(info == {})

    def test_basedbusplugin(self):
        voltverine_plugin = voltverine.plugins.BasePlugin()
        (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.DUNNO)
        self.assertTrue(info == {})

if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
