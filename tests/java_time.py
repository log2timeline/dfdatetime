#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the Java java.util.Date timestamp implementation."""

from __future__ import unicode_literals

import decimal
import unittest

from dfdatetime import java_time


class JavaTimeTest(unittest.TestCase):
  """Tests for the Java java.util.Date timestamp."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the properties."""
    java_time_object = java_time.JavaTime(timestamp=1281643591546)
    self.assertEqual(java_time_object.timestamp, 1281643591546)

    java_time_object = java_time.JavaTime()
    self.assertIsNone(java_time_object.timestamp)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    java_time_object = java_time.JavaTime(timestamp=1281643591546)

    normalized_timestamp = java_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281643591.546'))

    java_time_object = java_time.JavaTime()

    normalized_timestamp = java_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

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

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    java_time_object = java_time.JavaTime(timestamp=1281643591546)

    date_time_string = java_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31.546')

    java_time_object = java_time.JavaTime()

    date_time_string = java_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    java_time_object = java_time.JavaTime(timestamp=1281643591546)

    date_time_string = java_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.546Z')

  def testGetDate(self):
    """Tests the GetDate function."""
    java_time_object = java_time.JavaTime(timestamp=1281643591546)

    date_tuple = java_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    java_time_object = java_time.JavaTime()

    date_tuple = java_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    java_time_object = java_time.JavaTime(timestamp=1281643591546)

    time_of_day_tuple = java_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (20, 6, 31))

    java_time_object = java_time.JavaTime()

    time_of_day_tuple = java_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
