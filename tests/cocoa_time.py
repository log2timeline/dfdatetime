#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the Cocoa time implementation."""

import decimal
import unittest

from dfdatetime import cocoa_time


class CocoaTimeEpochTest(unittest.TestCase):
  """Tests for the Cocoa time epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    cocoa_time_epoch = cocoa_time.CocoaTimeEpoch()
    self.assertIsNotNone(cocoa_time_epoch)


class CocoaTimeTest(unittest.TestCase):
  """Tests for the Cocoa timestamp."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the properties."""
    cocoa_time_object = cocoa_time.CocoaTime(timestamp=395011845.0)
    self.assertEqual(cocoa_time_object.timestamp, 395011845.0)

    cocoa_time_object = cocoa_time.CocoaTime()
    self.assertIsNone(cocoa_time_object.timestamp)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    cocoa_time_object = cocoa_time.CocoaTime(timestamp=395011845.0)

    normalized_timestamp = cocoa_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1373319045.0'))

    cocoa_time_object = cocoa_time.CocoaTime(
        time_zone_offset=60, timestamp=395011845.0)

    normalized_timestamp = cocoa_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1373315445.0'))

    cocoa_time_object = cocoa_time.CocoaTime()

    normalized_timestamp = cocoa_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    cocoa_time_object = cocoa_time.CocoaTime()

    cocoa_time_object.CopyFromDateTimeString('2013-07-08')
    self.assertEqual(cocoa_time_object._timestamp, 394934400.0)
    self.assertEqual(cocoa_time_object._time_zone_offset, 0)

    cocoa_time_object.CopyFromDateTimeString('2013-07-08 21:30:45')
    self.assertEqual(cocoa_time_object._timestamp, 395011845.0)
    self.assertEqual(cocoa_time_object._time_zone_offset, 0)

    cocoa_time_object.CopyFromDateTimeString('2013-07-08 21:30:45.546875')
    self.assertEqual(cocoa_time_object._timestamp, 395011845.546875)
    self.assertEqual(cocoa_time_object._time_zone_offset, 0)

    cocoa_time_object.CopyFromDateTimeString('2013-07-08 21:30:45.546875-01:00')
    self.assertEqual(cocoa_time_object._timestamp, 395011845.546875)
    self.assertEqual(cocoa_time_object._time_zone_offset, -60)

    cocoa_time_object.CopyFromDateTimeString('2013-07-08 21:30:45.546875+01:00')
    self.assertEqual(cocoa_time_object._timestamp, 395011845.546875)
    self.assertEqual(cocoa_time_object._time_zone_offset, 60)

    cocoa_time_object.CopyFromDateTimeString('2001-01-02 00:00:00')
    self.assertEqual(cocoa_time_object._timestamp, 86400.0)
    self.assertEqual(cocoa_time_object._time_zone_offset, 0)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    cocoa_time_object = cocoa_time.CocoaTime(timestamp=395011845.546875)

    date_time_string = cocoa_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2013-07-08 21:30:45.546875')

    epoch_year = cocoa_time_object._EPOCH.year
    cocoa_time_object._EPOCH.year = -1

    with self.assertRaises(ValueError):
      cocoa_time_object.CopyToDateTimeString()

    cocoa_time_object._EPOCH.year = epoch_year

    cocoa_time_object = cocoa_time.CocoaTime()

    date_time_string = cocoa_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    cocoa_time_object = cocoa_time.CocoaTime(timestamp=395011845.546875)

    date_time_string = cocoa_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2013-07-08T21:30:45.546875+00:00')

  def testGetDate(self):
    """Tests the GetDate function."""
    cocoa_time_object = cocoa_time.CocoaTime(timestamp=395011845.546875)

    date_tuple = cocoa_time_object.GetDate()
    self.assertEqual(date_tuple, (2013, 7, 8))

    cocoa_time_object = cocoa_time.CocoaTime()

    date_tuple = cocoa_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    cocoa_time_object = cocoa_time.CocoaTime(timestamp=395011845.546875)

    date_with_time_of_day_tuple = cocoa_time_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2013, 7, 8, 21, 30, 45))

    cocoa_time_object = cocoa_time.CocoaTime()

    date_with_time_of_day_tuple = cocoa_time_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

  # TODO: remove this method when there is no more need for it in plaso.
  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    cocoa_time_object = cocoa_time.CocoaTime(timestamp=395011845.0)

    micro_posix_timestamp = cocoa_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, 1373319045000000)

    cocoa_time_object = cocoa_time.CocoaTime()

    micro_posix_timestamp = cocoa_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    cocoa_time_object = cocoa_time.CocoaTime(timestamp=395011845.546875)

    time_of_day_tuple = cocoa_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (21, 30, 45))

    cocoa_time_object = cocoa_time.CocoaTime()

    time_of_day_tuple = cocoa_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
