#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the WebKit timestamp implementation."""

import unittest

from dfdatetime import webkit_time


class WebKitTimeTest(unittest.TestCase):
  """Tests for the WebKit timestamp."""

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    webkit_time_object = webkit_time.WebKitTime()

    expected_timestamp = 12926044800000000
    webkit_time_object.CopyFromString(u'2010-08-12')
    self.assertEqual(webkit_time_object.timestamp, expected_timestamp)

    expected_timestamp = 12926120791000000
    webkit_time_object.CopyFromString(u'2010-08-12 21:06:31')
    self.assertEqual(webkit_time_object.timestamp, expected_timestamp)

    expected_timestamp = 12926120791546875
    webkit_time_object.CopyFromString(u'2010-08-12 21:06:31.546875')
    self.assertEqual(webkit_time_object.timestamp, expected_timestamp)

    expected_timestamp = 12926124391546875
    webkit_time_object.CopyFromString(u'2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(webkit_time_object.timestamp, expected_timestamp)

    expected_timestamp = 12926117191546875
    webkit_time_object.CopyFromString(u'2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(webkit_time_object.timestamp, expected_timestamp)

    expected_timestamp = 86400 * 1000000
    webkit_time_object.CopyFromString(u'1601-01-02 00:00:00')
    self.assertEqual(webkit_time_object.timestamp, expected_timestamp)

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    webkit_time_object = webkit_time.WebKitTime(timestamp=12926120791546875)

    expected_stat_time_tuple = (1281647191, 5468750)
    stat_time_tuple = webkit_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    webkit_time_object = webkit_time.WebKitTime(timestamp=0x1ffffffffffffffff)

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = webkit_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    webkit_time_object = webkit_time.WebKitTime()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = webkit_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    webkit_time_object = webkit_time.WebKitTime(timestamp=12926120791546875)

    expected_micro_posix_timestamp = 1281647191546875
    micro_posix_timestamp = webkit_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

    webkit_time_object = webkit_time.WebKitTime(timestamp=0x1ffffffffffffffff)

    micro_posix_timestamp = webkit_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)

    webkit_time_object = webkit_time.WebKitTime()

    micro_posix_timestamp = webkit_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
