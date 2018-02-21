#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the WebKit time implementation."""

from __future__ import unicode_literals

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

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    webkit_time_object = webkit_time.WebKitTime(timestamp=12926120791546875)

    stat_time_tuple = webkit_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (1281647191, 5468750))

    webkit_time_object = webkit_time.WebKitTime(timestamp=0x1ffffffffffffffff)

    stat_time_tuple = webkit_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

    webkit_time_object = webkit_time.WebKitTime()

    stat_time_tuple = webkit_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    webkit_time_object = webkit_time.WebKitTime(timestamp=12926120791546875)

    date_time_string = webkit_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 21:06:31.546875')

    webkit_time_object = webkit_time.WebKitTime()

    date_time_string = webkit_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testGetDate(self):
    """Tests the GetDate function."""
    webkit_time_object = webkit_time.WebKitTime(timestamp=12926120791546875)

    date_tuple = webkit_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    webkit_time_object._EPOCH.year = -1

    date_tuple = webkit_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

    webkit_time_object = webkit_time.WebKitTime()

    date_tuple = webkit_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    webkit_time_object = webkit_time.WebKitTime(timestamp=12926120791546875)

    micro_posix_timestamp = webkit_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, 1281647191546875)

    webkit_time_object = webkit_time.WebKitTime(timestamp=0x1ffffffffffffffff)

    micro_posix_timestamp = webkit_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)

    webkit_time_object = webkit_time.WebKitTime()

    micro_posix_timestamp = webkit_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
