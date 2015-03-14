import unittest
import sys
import dbusmock
import subprocess
try:
    from unittest import mock
except:
    import mock

import voltverine.plugins

class TestLogind(dbusmock.DBusTestCase):

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

    def test_uptime_10minutes(self):
        voltverine_plugin = voltverine.plugins.Uptime()
        with mock.patch('voltverine.plugins.uptime.open', mock.mock_open(read_data='600.0 0'), create=True) as m:
            (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.NOT_OK)
        self.assertEquals(info, {'uptime': 600.0})

    def test_uptime_10hours(self):
        voltverine_plugin = voltverine.plugins.Uptime()
        with mock.patch('voltverine.plugins.uptime.open', mock.mock_open(read_data='36000.0 0'), create=True) as m:
            (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.OK)
        self.assertEquals(info, {'uptime': 36000.0})

if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
