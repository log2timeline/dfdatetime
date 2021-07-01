#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the SYSTEMTIME structure implementation."""

import decimal
import unittest

from dfdatetime import systemtime


class SystemtimeTest(unittest.TestCase):
  """Tests for the SYSTEMTIME structure."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the initialization function."""
    systemtime_object = systemtime.Systemtime()
    self.assertIsNotNone(systemtime_object)

    systemtime_object = systemtime.Systemtime(
        system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 142))
    self.assertIsNotNone(systemtime_object)
    self.assertEqual(systemtime_object.year, 2010)
    self.assertEqual(systemtime_object.month, 8)
    self.assertEqual(systemtime_object.day_of_month, 12)
    self.assertEqual(systemtime_object.hours, 20)
    self.assertEqual(systemtime_object.minutes, 6)
    self.assertEqual(systemtime_object.seconds, 31)
    self.assertEqual(systemtime_object.milliseconds, 142)

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 4, 12, 20, 6, 31))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(1500, 8, 4, 12, 20, 6, 31, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 13, 4, 12, 20, 6, 31, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 7, 12, 20, 6, 31, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 4, 32, 20, 6, 31, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 4, 12, 24, 6, 31, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 4, 12, 20, 61, 31, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 4, 12, 20, 6, 61, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 1001))

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    systemtime_object = systemtime.Systemtime(
        system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 142))

    normalized_timestamp = systemtime_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281643591.142'))

    systemtime_object = systemtime.Systemtime(
        system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 142),
        time_zone_offset=60)

    normalized_timestamp = systemtime_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281639991.142'))

    systemtime_object = systemtime.Systemtime()

    normalized_timestamp = systemtime_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    systemtime_object = systemtime.Systemtime()

    systemtime_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(systemtime_object._number_of_seconds, 1281571200)
    self.assertEqual(systemtime_object._time_zone_offset, 0)
    self.assertEqual(systemtime_object.year, 2010)
    self.assertEqual(systemtime_object.month, 8)
    self.assertEqual(systemtime_object.day_of_month, 12)
    self.assertEqual(systemtime_object.hours, 0)
    self.assertEqual(systemtime_object.minutes, 0)
    self.assertEqual(systemtime_object.seconds, 0)
    self.assertEqual(systemtime_object.milliseconds, 0)

    systemtime_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(systemtime_object._number_of_seconds, 1281647191)
    self.assertEqual(systemtime_object._time_zone_offset, 0)
    self.assertEqual(systemtime_object.year, 2010)
    self.assertEqual(systemtime_object.month, 8)
    self.assertEqual(systemtime_object.day_of_month, 12)
    self.assertEqual(systemtime_object.hours, 21)
    self.assertEqual(systemtime_object.minutes, 6)
    self.assertEqual(systemtime_object.seconds, 31)
    self.assertEqual(systemtime_object.milliseconds, 0)

    systemtime_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(systemtime_object._number_of_seconds, 1281647191)
    self.assertEqual(systemtime_object._time_zone_offset, 0)
    self.assertEqual(systemtime_object.year, 2010)
    self.assertEqual(systemtime_object.month, 8)
    self.assertEqual(systemtime_object.day_of_month, 12)
    self.assertEqual(systemtime_object.hours, 21)
    self.assertEqual(systemtime_object.minutes, 6)
    self.assertEqual(systemtime_object.seconds, 31)
    self.assertEqual(systemtime_object.milliseconds, 546)

    systemtime_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(systemtime_object._number_of_seconds, 1281647191)
    self.assertEqual(systemtime_object._time_zone_offset, -60)
    self.assertEqual(systemtime_object.year, 2010)
    self.assertEqual(systemtime_object.month, 8)
    self.assertEqual(systemtime_object.day_of_month, 12)
    self.assertEqual(systemtime_object.hours, 21)
    self.assertEqual(systemtime_object.minutes, 6)
    self.assertEqual(systemtime_object.seconds, 31)
    self.assertEqual(systemtime_object.milliseconds, 546)
    self.assertEqual(systemtime_object.time_zone_offset, -60)

    systemtime_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(systemtime_object._number_of_seconds, 1281647191)
    self.assertEqual(systemtime_object._time_zone_offset, 60)
    self.assertEqual(systemtime_object.year, 2010)
    self.assertEqual(systemtime_object.month, 8)
    self.assertEqual(systemtime_object.day_of_month, 12)
    self.assertEqual(systemtime_object.hours, 21)
    self.assertEqual(systemtime_object.minutes, 6)
    self.assertEqual(systemtime_object.seconds, 31)
    self.assertEqual(systemtime_object.milliseconds, 546)
    self.assertEqual(systemtime_object.time_zone_offset, 60)

    systemtime_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(systemtime_object._number_of_seconds, -11644387200)
    self.assertEqual(systemtime_object._time_zone_offset, 0)
    self.assertEqual(systemtime_object.year, 1601)
    self.assertEqual(systemtime_object.month, 1)
    self.assertEqual(systemtime_object.day_of_month, 2)
    self.assertEqual(systemtime_object.hours, 0)
    self.assertEqual(systemtime_object.minutes, 0)
    self.assertEqual(systemtime_object.seconds, 0)
    self.assertEqual(systemtime_object.milliseconds, 0)

    with self.assertRaises(ValueError):
      systemtime_object.CopyFromDateTimeString('1600-01-02 00:00:00')

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    systemtime_object = systemtime.Systemtime(
        system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 142))

    date_time_string = systemtime_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31.142')

    systemtime_object = systemtime.Systemtime()

    date_time_string = systemtime_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    systemtime_object = systemtime.Systemtime(
        system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 142))

    date_time_string = systemtime_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.142+00:00')

  def testGetDate(self):
    """Tests the GetDate function."""
    systemtime_object = systemtime.Systemtime(
        system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 142))

    date_tuple = systemtime_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    systemtime_object = systemtime.Systemtime()

    date_tuple = systemtime_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    systemtime_object = systemtime.Systemtime(
        system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 142))

    date_with_time_of_day_tuple = systemtime_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2010, 8, 12, 20, 6, 31))

    systemtime_object = systemtime.Systemtime()

    date_with_time_of_day_tuple = systemtime_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    systemtime_object = systemtime.Systemtime(
        system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 142))

    time_of_day_tuple = systemtime_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (20, 6, 31))

    systemtime_object = systemtime.Systemtime()

    time_of_day_tuple = systemtime_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
