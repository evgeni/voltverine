import unittest
import sys
import os

try:
    from unittest import mock
except:
    import mock

import voltverine.plugins

class TestCommand(unittest.TestCase):

    def test_no_command_provided(self):
        voltverine_plugin = voltverine.plugins.Command()
        (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.DUNNO)
        self.assertTrue(info == {})

    def test_bad_command_provided(self):
        with mock.patch('subprocess.call', side_effect=OSError):
            voltverine_plugin = voltverine.plugins.Command(command='/bin/nothing')
            (action, info) = voltverine_plugin.analyze()
            self.assertTrue(action == voltverine.plugins.DUNNO)
            self.assertTrue(info == {})

    def test_command_ok(self):
        with mock.patch('subprocess.call', return_value=0):
            voltverine_plugin = voltverine.plugins.Command('/bin/true')
            (action, info) = voltverine_plugin.analyze()
            self.assertTrue(action == voltverine.plugins.OK)
            self.assertTrue(info == {'retcode': 0})

    def test_command_notok(self):
        with mock.patch('subprocess.call', return_value=1):
            voltverine_plugin = voltverine.plugins.Command('/bin/false')
            (action, info) = voltverine_plugin.analyze()
            self.assertTrue(action == voltverine.plugins.NOT_OK)
            self.assertTrue(info == {'retcode': 1})

    def test_command_ok_list(self):
        with mock.patch('subprocess.call', return_value=0):
            voltverine_plugin = voltverine.plugins.Command(['/bin/true'])
            (action, info) = voltverine_plugin.analyze()
            self.assertTrue(action == voltverine.plugins.OK)
            self.assertTrue(info == {'retcode': 0})

    def test_command_notok_li(self):
        with mock.patch('subprocess.call', return_value=1):
            voltverine_plugin = voltverine.plugins.Command(['/bin/false'])
            (action, info) = voltverine_plugin.analyze()
            self.assertTrue(action == voltverine.plugins.NOT_OK)
            self.assertTrue(info == {'retcode': 1})

if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
