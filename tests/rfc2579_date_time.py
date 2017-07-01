#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the RFC2579 date-time implementation."""

from __future__ import unicode_literals

import unittest

from dfdatetime import rfc2579_date_time


class RFC2579DateTimeInvalidYear(rfc2579_date_time.RFC2579DateTime):
  """RFC2579 date-time for testing invalid year in CopyFromString."""

  def _CopyDateTimeFromString(self, unused_time_string):
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
    self.assertEqual(rfc2579_date_time_object.hours, 18)
    self.assertEqual(rfc2579_date_time_object.minutes, 6)
    self.assertEqual(rfc2579_date_time_object.seconds, 31)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 6)

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

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime()

    expected_number_of_seconds = 1281571200
    rfc2579_date_time_object.CopyFromString('2010-08-12')
    self.assertEqual(
        rfc2579_date_time_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(rfc2579_date_time_object.year, 2010)
    self.assertEqual(rfc2579_date_time_object.month, 8)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 12)
    self.assertEqual(rfc2579_date_time_object.hours, 0)
    self.assertEqual(rfc2579_date_time_object.minutes, 0)
    self.assertEqual(rfc2579_date_time_object.seconds, 0)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 0)

    expected_number_of_seconds = 1281647191
    rfc2579_date_time_object.CopyFromString('2010-08-12 21:06:31')
    self.assertEqual(
        rfc2579_date_time_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(rfc2579_date_time_object.year, 2010)
    self.assertEqual(rfc2579_date_time_object.month, 8)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 12)
    self.assertEqual(rfc2579_date_time_object.hours, 21)
    self.assertEqual(rfc2579_date_time_object.minutes, 6)
    self.assertEqual(rfc2579_date_time_object.seconds, 31)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 0)

    expected_number_of_seconds = 1281647191
    rfc2579_date_time_object.CopyFromString('2010-08-12 21:06:31.546875')
    self.assertEqual(
        rfc2579_date_time_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(rfc2579_date_time_object.year, 2010)
    self.assertEqual(rfc2579_date_time_object.month, 8)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 12)
    self.assertEqual(rfc2579_date_time_object.hours, 21)
    self.assertEqual(rfc2579_date_time_object.minutes, 6)
    self.assertEqual(rfc2579_date_time_object.seconds, 31)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 5)

    expected_number_of_seconds = 1281650791
    rfc2579_date_time_object.CopyFromString('2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        rfc2579_date_time_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(rfc2579_date_time_object.year, 2010)
    self.assertEqual(rfc2579_date_time_object.month, 8)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 12)
    self.assertEqual(rfc2579_date_time_object.hours, 22)
    self.assertEqual(rfc2579_date_time_object.minutes, 6)
    self.assertEqual(rfc2579_date_time_object.seconds, 31)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 5)

    expected_number_of_seconds = 1281643591
    rfc2579_date_time_object.CopyFromString('2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        rfc2579_date_time_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(rfc2579_date_time_object.year, 2010)
    self.assertEqual(rfc2579_date_time_object.month, 8)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 12)
    self.assertEqual(rfc2579_date_time_object.hours, 20)
    self.assertEqual(rfc2579_date_time_object.minutes, 6)
    self.assertEqual(rfc2579_date_time_object.seconds, 31)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 5)

    expected_number_of_seconds = -11644387200
    rfc2579_date_time_object.CopyFromString('1601-01-02 00:00:00')
    self.assertEqual(
        rfc2579_date_time_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(rfc2579_date_time_object.year, 1601)
    self.assertEqual(rfc2579_date_time_object.month, 1)
    self.assertEqual(rfc2579_date_time_object.day_of_month, 2)
    self.assertEqual(rfc2579_date_time_object.hours, 0)
    self.assertEqual(rfc2579_date_time_object.minutes, 0)
    self.assertEqual(rfc2579_date_time_object.seconds, 0)
    self.assertEqual(rfc2579_date_time_object.deciseconds, 0)

    rfc2579_date_time_object = RFC2579DateTimeInvalidYear()

    with self.assertRaises(ValueError):
      rfc2579_date_time_object.CopyFromString('9999-01-02 00:00:00')

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime(
        rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 0, 0))

    expected_stat_time_tuple = (1281643591, 6000000)
    stat_time_tuple = rfc2579_date_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = rfc2579_date_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime(
        rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 0, 0))

    expected_micro_posix_number_of_seconds = 1281643591600000
    micro_posix_number_of_seconds = rfc2579_date_time_object.GetPlasoTimestamp()
    self.assertEqual(
        micro_posix_number_of_seconds, expected_micro_posix_number_of_seconds)

    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime()

    micro_posix_number_of_seconds = rfc2579_date_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_number_of_seconds)


if __name__ == '__main__':
  unittest.main()
