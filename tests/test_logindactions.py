import unittest
import sys
import dbus
import dbusmock
import subprocess
import os
import fcntl

import voltverine.actions

class TestLogindActions(dbusmock.DBusTestCase):

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
        voltverine_action = voltverine.actions.LogindPoweroff()
        voltverine_action.execute()

    def test_poweroff(self):
        (self.p_mock, obj_logind) = self.spawn_server_template('logind', {}, stdout=subprocess.PIPE)
        # set log to nonblocking
        #flags = fcntl.fcntl(self.p_mock.stdout, fcntl.F_GETFL)
        #fcntl.fcntl(self.p_mock.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        voltverine_action = voltverine.actions.LogindPoweroff()
        voltverine_action.execute()
        #this should work, but it blocks
        #self.assertRegex(self.p_mock.stdout.readline(), b'^[0-9.]+ Poweroff$')


if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
