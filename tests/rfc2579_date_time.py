#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the RFC2579 date-time implementation."""

import decimal
import unittest

from dfdatetime import rfc2579_date_time


class RFC2579DateTimeInvalidYear(rfc2579_date_time.RFC2579DateTime):
  """RFC2579 date-time for testing invalid year."""

  def _CopyDateTimeFromString(self, time_string):
    """Copies a date and time from a string.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Returns:
      dict[str, int]: date and time values, such as year, month, day of month,
          hours, minutes, seconds, microseconds.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    return {
        'year': 70000,
        'month': 1,
        'day_of_month': 2,
        'hours': 0,
        'minutes': 0,
        'seconds': 0}


class RFC2579DateTimeTest(unittest.TestCase):
  """Tests for the RFC2579 date-time."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the initialization function."""
    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime()
    self.assertIsNotNone(rfc2579_date_time_object)

    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime(
        rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 2, 0))
    self.assertIsNotNone(rfc2579_date_time_object)
    self.assertEqual(rfc2579_date_time_object.year, 2010)
    self.assertEqual(rfc2579_date_time_object.month, 8)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 12)
    self.assertEqual(rfc2579_date_time_object.hours, 20)
    self.assertEqual(rfc2579_date_time_object.minutes, 6)
    self.assertEqual(rfc2579_date_time_object.seconds, 31)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 6)
    self.assertEqual(rfc2579_date_time_object.time_zone_offset, 120)

    with self.assertRaises(ValueError):
      rfc2579_date_time.RFC2579DateTime(
          rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31))

    with self.assertRaises(ValueError):
      rfc2579_date_time.RFC2579DateTime(
          rfc2579_date_time_tuple=(65537, 8, 12, 20, 6, 31, 6, '+', 2, 0))

    with self.assertRaises(ValueError):
      rfc2579_date_time.RFC2579DateTime(
          rfc2579_date_time_tuple=(2010, 13, 12, 20, 6, 31, 6, '+', 2, 0))

    with self.assertRaises(ValueError):
      rfc2579_date_time.RFC2579DateTime(
          rfc2579_date_time_tuple=(2010, 8, 32, 20, 6, 31, 6, '+', 2, 0))

    with self.assertRaises(ValueError):
      rfc2579_date_time.RFC2579DateTime(
          rfc2579_date_time_tuple=(2010, 8, 12, 24, 6, 31, 6, '+', 2, 0))

    with self.assertRaises(ValueError):
      rfc2579_date_time.RFC2579DateTime(
          rfc2579_date_time_tuple=(2010, 8, 12, 20, 61, 31, 6, '+', 2, 0))

    with self.assertRaises(ValueError):
      rfc2579_date_time.RFC2579DateTime(
          rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 61, 6, '+', 2, 0))

    with self.assertRaises(ValueError):
      rfc2579_date_time.RFC2579DateTime(
          rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 11, '+', 2, 0))

    with self.assertRaises(ValueError):
      rfc2579_date_time.RFC2579DateTime(
          rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '#', 2, 0))

    with self.assertRaises(ValueError):
      rfc2579_date_time.RFC2579DateTime(
          rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 14, 0))

    with self.assertRaises(ValueError):
      rfc2579_date_time.RFC2579DateTime(
          rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 2, 60))

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime(
        rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 0, 0))

    normalized_timestamp = rfc2579_date_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281643591.6'))

    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime(
        rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 1, 0))

    normalized_timestamp = rfc2579_date_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281639991.6'))

    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime()

    normalized_timestamp = rfc2579_date_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime()

    rfc2579_date_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(rfc2579_date_time_object._number_of_seconds, 1281571200)
    self.assertEqual(rfc2579_date_time_object._time_zone_offset, 0)
    self.assertEqual(rfc2579_date_time_object.year, 2010)
    self.assertEqual(rfc2579_date_time_object.month, 8)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 12)
    self.assertEqual(rfc2579_date_time_object.hours, 0)
    self.assertEqual(rfc2579_date_time_object.minutes, 0)
    self.assertEqual(rfc2579_date_time_object.seconds, 0)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 0)

    rfc2579_date_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(rfc2579_date_time_object._number_of_seconds, 1281647191)
    self.assertEqual(rfc2579_date_time_object._time_zone_offset, 0)
    self.assertEqual(rfc2579_date_time_object.year, 2010)
    self.assertEqual(rfc2579_date_time_object.month, 8)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 12)
    self.assertEqual(rfc2579_date_time_object.hours, 21)
    self.assertEqual(rfc2579_date_time_object.minutes, 6)
    self.assertEqual(rfc2579_date_time_object.seconds, 31)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 0)

    rfc2579_date_time_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875')
    self.assertEqual(rfc2579_date_time_object._number_of_seconds, 1281647191)
    self.assertEqual(rfc2579_date_time_object._time_zone_offset, 0)
    self.assertEqual(rfc2579_date_time_object.year, 2010)
    self.assertEqual(rfc2579_date_time_object.month, 8)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 12)
    self.assertEqual(rfc2579_date_time_object.hours, 21)
    self.assertEqual(rfc2579_date_time_object.minutes, 6)
    self.assertEqual(rfc2579_date_time_object.seconds, 31)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 5)

    rfc2579_date_time_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(rfc2579_date_time_object._number_of_seconds, 1281647191)
    self.assertEqual(rfc2579_date_time_object._time_zone_offset, -60)
    self.assertEqual(rfc2579_date_time_object.year, 2010)
    self.assertEqual(rfc2579_date_time_object.month, 8)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 12)
    self.assertEqual(rfc2579_date_time_object.hours, 21)
    self.assertEqual(rfc2579_date_time_object.minutes, 6)
    self.assertEqual(rfc2579_date_time_object.seconds, 31)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 5)
    self.assertEqual(rfc2579_date_time_object.time_zone_offset, -60)

    rfc2579_date_time_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(rfc2579_date_time_object._number_of_seconds, 1281647191)
    self.assertEqual(rfc2579_date_time_object._time_zone_offset, 60)
    self.assertEqual(rfc2579_date_time_object.year, 2010)
    self.assertEqual(rfc2579_date_time_object.month, 8)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 12)
    self.assertEqual(rfc2579_date_time_object.hours, 21)
    self.assertEqual(rfc2579_date_time_object.minutes, 6)
    self.assertEqual(rfc2579_date_time_object.seconds, 31)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 5)
    self.assertEqual(rfc2579_date_time_object.time_zone_offset, 60)

    rfc2579_date_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(rfc2579_date_time_object._number_of_seconds, -11644387200)
    self.assertEqual(rfc2579_date_time_object._time_zone_offset, 0)
    self.assertEqual(rfc2579_date_time_object.year, 1601)
    self.assertEqual(rfc2579_date_time_object.month, 1)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 2)
    self.assertEqual(rfc2579_date_time_object.hours, 0)
    self.assertEqual(rfc2579_date_time_object.minutes, 0)
    self.assertEqual(rfc2579_date_time_object.seconds, 0)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 0)

    rfc2579_date_time_object = RFC2579DateTimeInvalidYear()

    with self.assertRaises(ValueError):
      rfc2579_date_time_object.CopyFromDateTimeString('9999-01-02 00:00:00')

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime(
        rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 0, 0))

    date_time_string = rfc2579_date_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31.6')

    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime()

    date_time_string = rfc2579_date_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime(
        rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 0, 0))

    date_time_string = rfc2579_date_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.6+00:00')

  def testGetDate(self):
    """Tests the GetDate function."""
    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime(
        rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 0, 0))

    date_tuple = rfc2579_date_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime()

    date_tuple = rfc2579_date_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime(
        rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 0, 0))

    date_with_time_of_day_tuple = (
        rfc2579_date_time_object.GetDateWithTimeOfDay())
    self.assertEqual(date_with_time_of_day_tuple, (2010, 8, 12, 20, 6, 31))

    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime()

    date_with_time_of_day_tuple = (
        rfc2579_date_time_object.GetDateWithTimeOfDay())
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime(
        rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 0, 0))

    time_of_day_tuple = rfc2579_date_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (20, 6, 31))

    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime()

    time_of_day_tuple = rfc2579_date_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
