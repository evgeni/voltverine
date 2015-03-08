import unittest
import sys
import dbusmock
import subprocess
import os
import fcntl

import voltverine.actions

class TestBaseAction(dbusmock.DBusTestCase):

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

    def test_baseaction(self):
        voltverine_action = voltverine.actions.BaseAction()
        voltverine_action.execute()

    def test_basedbusaction(self):
        voltverine_action = voltverine.actions.BaseDbusAction()
        voltverine_action.execute()

if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
