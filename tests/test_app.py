import unittest
import sys
import dbus
import dbusmock
import subprocess

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

    def test_help(self):
        with self.assertRaises(SystemExit) as cm:
            sys.argv = ['voltverine', '-h']
            v = voltverine.app.VoltverineApp()
        output = sys.stdout.getvalue().strip() # because stdout is an StringIO instance
        self.assertRegex(output, 'usage')
        self.assertRegex(output, 'voltverine')
        self.assertEquals(cm.exception.code, 0)


if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
