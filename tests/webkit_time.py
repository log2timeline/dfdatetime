#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the WebKit time implementation."""

from __future__ import unicode_literals

import decimal
import unittest

from dfdatetime import webkit_time


class WebKitTimeEpochTest(unittest.TestCase):
  """Tests for the WebKit time epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    webkit_epoch = webkit_time.WebKitTimeEpoch()
    self.assertIsNotNone(webkit_epoch)


class WebKitTimeTest(unittest.TestCase):
  """Tests for the WebKit timestamp."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the properties."""
    webkit_time_object = webkit_time.WebKitTime(timestamp=12926120791546875)
    self.assertEqual(webkit_time_object.timestamp, 12926120791546875)

    webkit_time_object = webkit_time.WebKitTime()
    self.assertIsNone(webkit_time_object.timestamp)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    webkit_time_object = webkit_time.WebKitTime(timestamp=12926120791546875)

    normalized_timestamp = webkit_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281647191.546875'))

    webkit_time_object = webkit_time.WebKitTime(timestamp=0x1ffffffffffffffff)

    normalized_timestamp = webkit_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

    webkit_time_object = webkit_time.WebKitTime()

    normalized_timestamp = webkit_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    webkit_time_object = webkit_time.WebKitTime()

    expected_timestamp = 12926044800000000
    webkit_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(webkit_time_object.timestamp, expected_timestamp)

    expected_timestamp = 12926120791000000
    webkit_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(webkit_time_object.timestamp, expected_timestamp)

    expected_timestamp = 12926120791546875
    webkit_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(webkit_time_object.timestamp, expected_timestamp)

    expected_timestamp = 12926124391546875
    webkit_time_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(webkit_time_object.timestamp, expected_timestamp)

    expected_timestamp = 12926117191546875
    webkit_time_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(webkit_time_object.timestamp, expected_timestamp)

    expected_timestamp = 86400 * 1000000
    webkit_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(webkit_time_object.timestamp, expected_timestamp)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    webkit_time_object = webkit_time.WebKitTime(timestamp=12926120791546875)

    date_time_string = webkit_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 21:06:31.546875')

    webkit_time_object = webkit_time.WebKitTime()

    date_time_string = webkit_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    webkit_time_object = webkit_time.WebKitTime(timestamp=12926120791546875)

    date_time_string = webkit_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T21:06:31.546875Z')

  def testGetDate(self):
    """Tests the GetDate function."""
    webkit_time_object = webkit_time.WebKitTime(timestamp=12926120791546875)

    date_tuple = webkit_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    webkit_time_object = webkit_time.WebKitTime()

    date_tuple = webkit_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    webkit_time_object = webkit_time.WebKitTime(timestamp=12926120791546875)

    time_of_day_tuple = webkit_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (21, 6, 31))

    webkit_time_object = webkit_time.WebKitTime()

    time_of_day_tuple = webkit_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
