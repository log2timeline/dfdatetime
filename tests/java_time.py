#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Java java.util.Date timestamp implementation."""

import unittest

from dfdatetime import java_time


class JavaTimeTest(unittest.TestCase):
  """Tests for the Java java.util.Date timestamp."""

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    java_time_object = java_time.JavaTime()

    expected_timestamp = 1281571200000
    java_time_object.CopyFromString(u'2010-08-12')
    self.assertEqual(java_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191000
    java_time_object.CopyFromString(u'2010-08-12 21:06:31')
    self.assertEqual(java_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191546
    java_time_object.CopyFromString(u'2010-08-12 21:06:31.546875')
    self.assertEqual(java_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281650791546
    java_time_object.CopyFromString(u'2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(java_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281643591546
    java_time_object.CopyFromString(u'2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(java_time_object.timestamp, expected_timestamp)

    expected_timestamp = -11644387200000
    java_time_object.CopyFromString(u'1601-01-02 00:00:00')
    self.assertEqual(java_time_object.timestamp, expected_timestamp)

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    java_time_object = java_time.JavaTime(timestamp=1281643591546)

    expected_stat_time_tuple = (1281643591, 5460000)
    stat_time_tuple = java_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    java_time_object = java_time.JavaTime()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = java_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    java_time_object = java_time.JavaTime(timestamp=1281643591546)

    expected_micro_posix_timestamp = 1281643591546000
    micro_posix_timestamp = java_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

    java_time_object = java_time.JavaTime()

    micro_posix_timestamp = java_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
