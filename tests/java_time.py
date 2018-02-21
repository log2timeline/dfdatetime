#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Java java.util.Date timestamp implementation."""

from __future__ import unicode_literals

import unittest

from dfdatetime import java_time


class JavaTimeTest(unittest.TestCase):
  """Tests for the Java java.util.Date timestamp."""

  # pylint: disable=protected-access

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    java_time_object = java_time.JavaTime()

    expected_timestamp = 1281571200000
    java_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(java_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191000
    java_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(java_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191546
    java_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(java_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281650791546
    java_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(java_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281643591546
    java_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(java_time_object.timestamp, expected_timestamp)

    expected_timestamp = -11644387200000
    java_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(java_time_object.timestamp, expected_timestamp)

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    java_time_object = java_time.JavaTime(timestamp=1281643591546)

    stat_time_tuple = java_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (1281643591, 5460000))

    java_time_object = java_time.JavaTime()

    stat_time_tuple = java_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    java_time_object = java_time.JavaTime(timestamp=1281643591546)

    date_time_string = java_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31.546')

    java_time_object = java_time.JavaTime()

    date_time_string = java_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testGetDate(self):
    """Tests the GetDate function."""
    java_time_object = java_time.JavaTime(timestamp=1281643591546)

    date_tuple = java_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    java_time_object._EPOCH.year = -1

    date_tuple = java_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

    java_time_object = java_time.JavaTime()

    date_tuple = java_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    java_time_object = java_time.JavaTime(timestamp=1281643591546)

    micro_posix_timestamp = java_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, 1281643591546000)

    java_time_object = java_time.JavaTime()

    micro_posix_timestamp = java_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
