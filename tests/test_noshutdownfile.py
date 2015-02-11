import unittest
import sys
import os

try:
    from unittest import mock
except:
    import mock

import voltverine.plugins

class TestNoShutdownFile(unittest.TestCase):

    def test_no_shutdownfile_provided(self):
        voltverine_plugin = voltverine.plugins.NoShutdownFile()
        (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.DUNNO)
        self.assertTrue(info == {})

    def test_no_shutdownfile(self):
        with mock.patch('os.path.exists', return_value=False):
            voltverine_plugin = voltverine.plugins.NoShutdownFile('/nonexistant/path')
            (action, info) = voltverine_plugin.analyze()
            self.assertTrue(action == voltverine.plugins.OK)
            self.assertTrue(info == {})

    def test_shutdownfile(self):
        with mock.patch('os.path.exists', return_value=True):
            voltverine_plugin = voltverine.plugins.NoShutdownFile('/existant/path')
            (action, info) = voltverine_plugin.analyze()
            self.assertTrue(action == voltverine.plugins.NOT_OK)
            self.assertTrue(info == {})

if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
