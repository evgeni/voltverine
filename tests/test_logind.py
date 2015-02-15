import unittest
import sys
import dbus
import dbusmock
import subprocess

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

    def test_no_logind(self):
        voltverine_plugin = voltverine.plugins.LogindSessions()
        (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.DUNNO)
        self.assertTrue(info == {})

    def test_no_inhibitor(self):
        (self.p_mock, obj_logind) = self.spawn_server_template('logind', {}, stdout=subprocess.PIPE)
        voltverine_plugin = voltverine.plugins.LogindInhibitors()
        (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.OK)
        self.assertTrue(info == {})

    @unittest.expectedFailure
    def test_inhibitor(self):
        (self.p_mock, obj_logind) = self.spawn_server_template('logind', {}, stdout=subprocess.PIPE)
        x = obj_logind.Inhibit('shutdown', 'unittest', 'running tests', 'block')
        voltverine_plugin = voltverine.plugins.LogindInhibitors()
        (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.NOT_OK)
        self.assertTrue(info == {'sessions': 1})

    def test_no_session(self):
        (self.p_mock, obj_logind) = self.spawn_server_template('logind', {}, stdout=subprocess.PIPE)
        voltverine_plugin = voltverine.plugins.LogindSessions()
        (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.OK)
        self.assertTrue(info == {})

    def test_session(self):
        (self.p_mock, obj_logind) = self.spawn_server_template('logind', {}, stdout=subprocess.PIPE)
        obj_logind.AddSession('c1', 'seat0', 500, 'joe', True)
        voltverine_plugin = voltverine.plugins.LogindSessions()
        (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.NOT_OK)
        self.assertTrue(info == {'sessions': 1})

if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
