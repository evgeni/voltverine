import unittest
import sys
import os
import datetime

try:
    from unittest import mock
except:
    import mock

import voltverine.plugins

class TestTime(unittest.TestCase):

    def test_no_time_provided(self):
        voltverine_plugin = voltverine.plugins.Time()
        (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.DUNNO)
        self.assertTrue(info == {})

    def test_bad_time_provided(self):
        voltverine_plugin = voltverine.plugins.Time(time={'start': 'garbage', 'end': 'pulp'})
        (action, info) = voltverine_plugin.analyze()
        self.assertTrue(action == voltverine.plugins.DUNNO)
        self.assertTrue(info == {})

    def test_time_ok(self):
        target = datetime.datetime(1900, 1, 1, 20, 00)
        with mock.patch.object(datetime, 'datetime', mock.Mock(wraps=datetime.datetime)) as patched:
            patched.now.return_value = target
            voltverine_plugin = voltverine.plugins.Time(time={'start': '9:00', 'end': '17:00'})
            (action, info) = voltverine_plugin.analyze()
            self.assertTrue(action == voltverine.plugins.OK)
            self.assertTrue(info == {})

    def test_time_notok(self):
        target = datetime.datetime(1900, 1, 1, 14, 00)
        with mock.patch.object(datetime, 'datetime', mock.Mock(wraps=datetime.datetime)) as patched:
            patched.now.return_value = target
            voltverine_plugin = voltverine.plugins.Time(time={'start': '9:00', 'end': '17:00'})
            (action, info) = voltverine_plugin.analyze()
            self.assertTrue(action == voltverine.plugins.NOT_OK)
            self.assertTrue(info == {})

    def test_time_list_ok(self):
        target = datetime.datetime(1900, 1, 1, 20, 00)
        with mock.patch.object(datetime, 'datetime', mock.Mock(wraps=datetime.datetime)) as patched:
            patched.now.return_value = target
            voltverine_plugin = voltverine.plugins.Time(time=[{'start': '9:00', 'end': '17:00'}])
            (action, info) = voltverine_plugin.analyze()
            self.assertTrue(action == voltverine.plugins.OK)
            self.assertTrue(info == {})

    def test_time_list_notok(self):
        target = datetime.datetime(1900, 1, 1, 14, 00)
        with mock.patch.object(datetime, 'datetime', mock.Mock(wraps=datetime.datetime)) as patched:
            patched.now.return_value = target
            voltverine_plugin = voltverine.plugins.Time(time=[{'start': '9:00', 'end': '17:00'}])
            (action, info) = voltverine_plugin.analyze()
            self.assertTrue(action == voltverine.plugins.NOT_OK)
            self.assertTrue(info == {})

if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
