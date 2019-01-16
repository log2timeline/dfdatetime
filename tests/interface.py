#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the date and time interfaces."""

from __future__ import unicode_literals

import unittest

from dfdatetime import interface


class EmptyDateTimeValues(interface.DateTimeValues):
  """Empty date time values for testing."""

  # pylint: disable=abstract-method,redundant-returns-doc

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      float: normalized timestamp, which is None for testing purposes.
    """
    return None


class TestDateTimeValues(interface.DateTimeValues):
  """Date time values for testing."""

  # pylint: disable=abstract-method

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      float: normalized timestamp, which is 0.0 for testing purposes.
    """
    return 0.0


class DateTimeEpochTest(unittest.TestCase):
  """Tests for the date and time epoch interface."""

  def testInitialize(self):
    """Tests the __init__ function."""
    date_time_epoch = interface.DateTimeEpoch(1970, 1, 1)
    self.assertIsNotNone(date_time_epoch)


class DateTimeValuesTest(unittest.TestCase):
  """Tests for the date and time values interface."""

  # pylint: disable=protected-access

  def testComparison(self):
    """Tests the comparison functions."""
    date_time_values1 = EmptyDateTimeValues()

    date_time_values2 = EmptyDateTimeValues()

    self.assertTrue(date_time_values1 == date_time_values2)
    self.assertTrue(date_time_values1 >= date_time_values2)
    self.assertFalse(date_time_values1 > date_time_values2)
    self.assertTrue(date_time_values1 <= date_time_values2)
    self.assertFalse(date_time_values1 < date_time_values2)
    self.assertFalse(date_time_values1 != date_time_values2)

    date_time_values1 = EmptyDateTimeValues()

    date_time_values2 = TestDateTimeValues()

    self.assertFalse(date_time_values1 == date_time_values2)
    self.assertFalse(date_time_values1 >= date_time_values2)
    self.assertFalse(date_time_values1 > date_time_values2)
    self.assertTrue(date_time_values1 <= date_time_values2)
    self.assertTrue(date_time_values1 < date_time_values2)
    self.assertTrue(date_time_values1 != date_time_values2)

    date_time_values1 = TestDateTimeValues()

    date_time_values2 = EmptyDateTimeValues()

    self.assertFalse(date_time_values1 == date_time_values2)
    self.assertTrue(date_time_values1 >= date_time_values2)
    self.assertTrue(date_time_values1 > date_time_values2)
    self.assertFalse(date_time_values1 <= date_time_values2)
    self.assertFalse(date_time_values1 < date_time_values2)
    self.assertTrue(date_time_values1 != date_time_values2)

    date_time_values1 = TestDateTimeValues()

    date_time_values2 = TestDateTimeValues()

    self.assertTrue(date_time_values1 == date_time_values2)
    self.assertTrue(date_time_values1 >= date_time_values2)
    self.assertFalse(date_time_values1 > date_time_values2)
    self.assertTrue(date_time_values1 <= date_time_values2)
    self.assertFalse(date_time_values1 < date_time_values2)
    self.assertFalse(date_time_values1 != date_time_values2)

    self.assertFalse(date_time_values1 == 0.0)

    with self.assertRaises(ValueError):
      date_time_values1 >= 0.0  # pylint: disable=pointless-statement

    with self.assertRaises(ValueError):
      date_time_values1 > 0.0  # pylint: disable=pointless-statement

    with self.assertRaises(ValueError):
      date_time_values1 <= 0.0  # pylint: disable=pointless-statement

    with self.assertRaises(ValueError):
      date_time_values1 < 0.0  # pylint: disable=pointless-statement

    self.assertTrue(date_time_values1 != 0.0)

  # TODO: add tests for _AdjustForTimeZoneOffset.

  def testCopyDateFromString(self):
    """Tests the _CopyDateFromString function."""
    date_time_values = interface.DateTimeValues()

    expected_date_tuple = (2010, 1, 1)
    date_tuple = date_time_values._CopyDateFromString('2010-01-01')
    self.assertEqual(date_tuple, expected_date_tuple)

    expected_date_tuple = (2010, 8, 1)
    date_tuple = date_time_values._CopyDateFromString('2010-08-01')
    self.assertEqual(date_tuple, expected_date_tuple)

    expected_date_tuple = (2010, 8, 12)
    date_tuple = date_time_values._CopyDateFromString('2010-08-12')
    self.assertEqual(date_tuple, expected_date_tuple)

    expected_date_tuple = (2010, 8, 31)
    date_tuple = date_time_values._CopyDateFromString('2010-08-31')
    self.assertEqual(date_tuple, expected_date_tuple)

    expected_date_tuple = (2010, 12, 31)
    date_tuple = date_time_values._CopyDateFromString('2010-12-31')
    self.assertEqual(date_tuple, expected_date_tuple)

    expected_date_tuple = (1601, 1, 2)
    date_tuple = date_time_values._CopyDateFromString('1601-01-02')
    self.assertEqual(date_tuple, expected_date_tuple)

    with self.assertRaises(ValueError):
      date_time_values._CopyDateFromString('')

    with self.assertRaises(ValueError):
      date_time_values._CopyDateFromString('195a-01-02')

    with self.assertRaises(ValueError):
      date_time_values._CopyDateFromString('10000-01-02')

    with self.assertRaises(ValueError):
      date_time_values._CopyDateFromString('2010-09-00')

    with self.assertRaises(ValueError):
      date_time_values._CopyDateFromString('2010-09-31')

    with self.assertRaises(ValueError):
      date_time_values._CopyDateFromString('1601-01-32')

    with self.assertRaises(ValueError):
      date_time_values._CopyDateFromString('1601-01-b2')

    with self.assertRaises(ValueError):
      date_time_values._CopyDateFromString('1601-13-02')

    with self.assertRaises(ValueError):
      date_time_values._CopyDateFromString('1601-a1-02')

    with self.assertRaises(ValueError):
      date_time_values._CopyDateFromString('2010-02-29')

    with self.assertRaises(ValueError):
      date_time_values._CopyDateFromString('2010-04-31')

  def testCopyDateTimeFromString(self):
    """Tests the _CopyDateTimeFromString function."""
    date_time_values = interface.DateTimeValues()

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12}
    date_dict = date_time_values._CopyDateTimeFromString('2010-08-12')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12,
        'hours': 21, 'minutes': 6, 'seconds': 31}
    date_dict = date_time_values._CopyDateTimeFromString(
        '2010-08-12 21:06:31')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12,
        'hours': 21, 'minutes': 6, 'seconds': 31, 'microseconds': 546875}
    date_dict = date_time_values._CopyDateTimeFromString(
        '2010-08-12 21:06:31.546875')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12,
        'hours': 22, 'minutes': 6, 'seconds': 31, 'microseconds': 546875}
    date_dict = date_time_values._CopyDateTimeFromString(
        '2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12,
        'hours': 20, 'minutes': 6, 'seconds': 31, 'microseconds': 546875}
    date_dict = date_time_values._CopyDateTimeFromString(
        '2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12,
        'hours': 20, 'minutes': 6, 'seconds': 31, 'microseconds': 546875}
    date_dict = date_time_values._CopyDateTimeFromString(
        '2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(date_dict, expected_date_dict)

    # Test backwards date correction.
    expected_date_dict = {
        'year': 2009, 'month': 12, 'day_of_month': 31,
        'hours': 23, 'minutes': 45, 'seconds': 0, 'microseconds': 123456}
    date_dict = date_time_values._CopyDateTimeFromString(
        '2010-01-01 00:15:00.123456+00:30')
    self.assertEqual(date_dict, expected_date_dict)

    # Test forward date correction.
    expected_date_dict = {
        'year': 2010, 'month': 1, 'day_of_month': 1,
        'hours': 1, 'minutes': 15, 'seconds': 0, 'microseconds': 123456}
    date_dict = date_time_values._CopyDateTimeFromString(
        '2009-12-31 23:45:00.123456-01:30')
    self.assertEqual(date_dict, expected_date_dict)

    with self.assertRaises(ValueError):
      date_time_values._CopyDateTimeFromString('')

    with self.assertRaises(ValueError):
      date_time_values._CopyDateTimeFromString(
          '2010-08-12T21:06:31.546875+01:00')

  def testCopyTimeFromString(self):
    """Tests the _CopyTimeFromString function."""
    date_time_values = interface.DateTimeValues()

    expected_time_tuple = (8, 4, 32, None, None)
    time_tuple = date_time_values._CopyTimeFromString('08:04:32')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, None, None)
    time_tuple = date_time_values._CopyTimeFromString('20:23:56')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, None, -330)
    time_tuple = date_time_values._CopyTimeFromString('20:23:56+05:30')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, 327000, None)
    time_tuple = date_time_values._CopyTimeFromString('20:23:56.327')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, 327000, -60)
    time_tuple = date_time_values._CopyTimeFromString('20:23:56.327+01:00')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, 327124, None)
    time_tuple = date_time_values._CopyTimeFromString('20:23:56.327124')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, 327124, 300)
    time_tuple = date_time_values._CopyTimeFromString('20:23:56.327124-05:00')
    self.assertEqual(time_tuple, expected_time_tuple)

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('14')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('14:00')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('24:00:00')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('12b00:00')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('12:00b00')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('1s:00:00')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('00:60:00')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('00:e0:00')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('00:00:60')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('00:00:w0')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('12:00:00.00')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('12:00:00.0000')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('12:00:00.00w')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('12:00:00+01b00')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('12:00:00+0w:00')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('12:00:00+20:00')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('12:00:00+01:0w')

    with self.assertRaises(ValueError):
      date_time_values._CopyTimeFromString('12:00:00+01:60')

  def testGetDateValues(self):
    """Tests the _GetDateValues function."""
    date_time_values = interface.DateTimeValues()

    year, month, day_of_month = date_time_values._GetDateValues(0, 2000, 1, 1)
    self.assertEqual(year, 2000)
    self.assertEqual(month, 1)
    self.assertEqual(day_of_month, 1)

    year, month, day_of_month = date_time_values._GetDateValues(10, 2000, 1, 1)
    self.assertEqual(year, 2000)
    self.assertEqual(month, 1)
    self.assertEqual(day_of_month, 11)

    year, month, day_of_month = date_time_values._GetDateValues(100, 2000, 1, 1)
    self.assertEqual(year, 2000)
    self.assertEqual(month, 4)
    self.assertEqual(day_of_month, 10)

    year, month, day_of_month = date_time_values._GetDateValues(100, 1999, 1, 1)
    self.assertEqual(year, 1999)
    self.assertEqual(month, 4)
    self.assertEqual(day_of_month, 11)

    year, month, day_of_month = date_time_values._GetDateValues(0, 1999, 12, 30)
    self.assertEqual(year, 1999)
    self.assertEqual(month, 12)
    self.assertEqual(day_of_month, 30)

    year, month, day_of_month = date_time_values._GetDateValues(5, 1999, 12, 30)
    self.assertEqual(year, 2000)
    self.assertEqual(month, 1)
    self.assertEqual(day_of_month, 4)

    year, month, day_of_month = date_time_values._GetDateValues(-10, 2000, 1, 1)
    self.assertEqual(year, 1999)
    self.assertEqual(month, 12)
    self.assertEqual(day_of_month, 22)

    year, month, day_of_month = date_time_values._GetDateValues(
        -100, 2000, 1, 1)
    self.assertEqual(year, 1999)
    self.assertEqual(month, 9)
    self.assertEqual(day_of_month, 23)

    year, month, day_of_month = date_time_values._GetDateValues(-10, 2000, 1, 9)
    self.assertEqual(year, 1999)
    self.assertEqual(month, 12)
    self.assertEqual(day_of_month, 30)

    with self.assertRaises(ValueError):
      date_time_values._GetDateValues(10, -1, 1, 1)

    with self.assertRaises(ValueError):
      date_time_values._GetDateValues(10, 2000, 0, 1)

    with self.assertRaises(ValueError):
      date_time_values._GetDateValues(10, 2000, 13, 1)

    with self.assertRaises(ValueError):
      date_time_values._GetDateValues(10, 2000, 1, 0)

    with self.assertRaises(ValueError):
      date_time_values._GetDateValues(10, 2000, 1, 32)

    year, month, day_of_month = date_time_values._GetDateValues(
        0, 1899, 12, 30)
    self.assertEqual(year, 1899)
    self.assertEqual(month, 12)
    self.assertEqual(day_of_month, 30)

    year, month, day_of_month = date_time_values._GetDateValues(
        25569, 1899, 12, 30)
    self.assertEqual(year, 1970)
    self.assertEqual(month, 1)
    self.assertEqual(day_of_month, 1)

    year, month, day_of_month = date_time_values._GetDateValues(
        36526, 1899, 12, 30)
    self.assertEqual(year, 2000)
    self.assertEqual(month, 1)
    self.assertEqual(day_of_month, 1)

    year, month, day_of_month = date_time_values._GetDateValues(
        41275, 1899, 12, 30)
    self.assertEqual(year, 2013)
    self.assertEqual(month, 1)
    self.assertEqual(day_of_month, 1)

    year, month, day_of_month = date_time_values._GetDateValues(
        41443, 1899, 12, 30)
    self.assertEqual(year, 2013)
    self.assertEqual(month, 6)
    self.assertEqual(day_of_month, 18)

    year, month, day_of_month = date_time_values._GetDateValues(
        -25569, 1899, 12, 30)
    self.assertEqual(year, 1829)
    self.assertEqual(month, 12)
    self.assertEqual(day_of_month, 28)

    year, month, day_of_month = date_time_values._GetDateValues(0, 1970, 1, 1)
    self.assertEqual(year, 1970)
    self.assertEqual(month, 1)
    self.assertEqual(day_of_month, 1)

    year, month, day_of_month = date_time_values._GetDateValues(-1, 1970, 1, 1)
    self.assertEqual(year, 1969)
    self.assertEqual(month, 12)
    self.assertEqual(day_of_month, 31)

    year, month, day_of_month = date_time_values._GetDateValues(364, 1970, 1, 1)
    self.assertEqual(year, 1970)
    self.assertEqual(month, 12)
    self.assertEqual(day_of_month, 31)

    year, month, day_of_month = date_time_values._GetDateValues(
        1460, 1970, 1, 1)
    self.assertEqual(year, 1973)
    self.assertEqual(month, 12)
    self.assertEqual(day_of_month, 31)

  def testGetDateValuesWithEpoch(self):
    """Tests the _GetDateValuesWithEpoch function."""
    date_time_epoch = interface.DateTimeEpoch(2000, 1, 1)
    date_time_values = interface.DateTimeValues()

    year, month, day_of_month = date_time_values._GetDateValuesWithEpoch(
        0, date_time_epoch)
    self.assertEqual(year, 2000)
    self.assertEqual(month, 1)
    self.assertEqual(day_of_month, 1)

  def testGetDayOfYear(self):
    """Tests the _GetDayOfYear function."""
    date_time_values = interface.DateTimeValues()

    day_of_year = date_time_values._GetDayOfYear(1999, 1, 1)
    self.assertEqual(day_of_year, 1)

    day_of_year = date_time_values._GetDayOfYear(1999, 4, 21)
    self.assertEqual(day_of_year, 111)

    day_of_year = date_time_values._GetDayOfYear(1999, 12, 31)
    self.assertEqual(day_of_year, 365)

    day_of_year = date_time_values._GetDayOfYear(2000, 1, 1)
    self.assertEqual(day_of_year, 1)

    day_of_year = date_time_values._GetDayOfYear(2000, 4, 21)
    self.assertEqual(day_of_year, 112)

    day_of_year = date_time_values._GetDayOfYear(2000, 12, 31)
    self.assertEqual(day_of_year, 366)

    with self.assertRaises(ValueError):
      date_time_values._GetDayOfYear(1999, 0, 1)

    with self.assertRaises(ValueError):
      date_time_values._GetDayOfYear(1999, 13, 1)

    with self.assertRaises(ValueError):
      date_time_values._GetDayOfYear(1999, 1, 0)

    with self.assertRaises(ValueError):
      date_time_values._GetDayOfYear(1999, 1, 32)

  def testGetDaysPerMonth(self):
    """Tests the _GetDaysPerMonth function."""
    date_time_values = interface.DateTimeValues()

    expected_days_per_month = list(interface.DateTimeValues._DAYS_PER_MONTH)

    days_per_month = []
    for month in range(1, 13):
      days_per_month.append(date_time_values._GetDaysPerMonth(1999, month))

    self.assertEqual(days_per_month, expected_days_per_month)

    expected_days_per_month[1] += 1

    days_per_month = []
    for month in range(1, 13):
      days_per_month.append(date_time_values._GetDaysPerMonth(2000, month))

    self.assertEqual(days_per_month, expected_days_per_month)

    with self.assertRaises(ValueError):
      date_time_values._GetDaysPerMonth(1999, 0)

    with self.assertRaises(ValueError):
      date_time_values._GetDaysPerMonth(1999, 13)

  def testGetNumberOfDaysInCentury(self):
    """Tests the _GetNumberOfDaysInCentury function."""
    date_time_values = interface.DateTimeValues()

    self.assertEqual(date_time_values._GetNumberOfDaysInCentury(1700), 36524)
    self.assertEqual(date_time_values._GetNumberOfDaysInCentury(2000), 36525)

    with self.assertRaises(ValueError):
      date_time_values._GetNumberOfDaysInCentury(-1)

  def testGetNumberOfDaysInYear(self):
    """Tests the _GetNumberOfDaysInYear function."""
    date_time_values = interface.DateTimeValues()

    self.assertEqual(date_time_values._GetNumberOfDaysInYear(1999), 365)
    self.assertEqual(date_time_values._GetNumberOfDaysInYear(2000), 366)
    self.assertEqual(date_time_values._GetNumberOfDaysInYear(1996), 366)

  def testGetNumberOfSecondsFromElements(self):
    """Tests the _GetNumberOfSecondsFromElements function."""
    date_time_values = interface.DateTimeValues()

    number_of_seconds = date_time_values._GetNumberOfSecondsFromElements(
        2010, 8, 12, 0, 0, 0)
    self.assertEqual(number_of_seconds, 1281571200)

    number_of_seconds = date_time_values._GetNumberOfSecondsFromElements(
        2010, 8, 12, None, None, None)
    self.assertEqual(number_of_seconds, 1281571200)

    number_of_seconds = date_time_values._GetNumberOfSecondsFromElements(
        2010, 8, 12, 21, 6, 31)
    self.assertEqual(number_of_seconds, 1281647191)

    number_of_seconds = date_time_values._GetNumberOfSecondsFromElements(
        1601, 1, 2, 0, 0, 0)
    self.assertEqual(number_of_seconds, -11644387200)

    number_of_seconds = date_time_values._GetNumberOfSecondsFromElements(
        0, 1, 2, 0, 0, 0)
    self.assertIsNone(number_of_seconds)

    with self.assertRaises(ValueError):
      date_time_values._GetNumberOfSecondsFromElements(2010, 13, 12, 21, 6, 31)

    with self.assertRaises(ValueError):
      date_time_values._GetNumberOfSecondsFromElements(2010, 13, 12, 24, 6, 31)

    with self.assertRaises(ValueError):
      date_time_values._GetNumberOfSecondsFromElements(2010, 13, 12, 21, 99, 31)

    with self.assertRaises(ValueError):
      date_time_values._GetNumberOfSecondsFromElements(2010, 13, 12, 21, 6, 65)

    with self.assertRaises(ValueError):
      date_time_values._GetNumberOfSecondsFromElements(2013, 2, 29, 1, 4, 25)

  def testGetTimeValues(self):
    """Tests the _GetTimeValues function."""
    date_time_values = interface.DateTimeValues()

    days, hours, minutes, seconds = date_time_values._GetTimeValues(10)
    self.assertEqual(days, 0)
    self.assertEqual(hours, 0)
    self.assertEqual(minutes, 0)
    self.assertEqual(seconds, 10)

    days, hours, minutes, seconds = date_time_values._GetTimeValues(190)
    self.assertEqual(days, 0)
    self.assertEqual(hours, 0)
    self.assertEqual(minutes, 3)
    self.assertEqual(seconds, 10)

    days, hours, minutes, seconds = date_time_values._GetTimeValues(18190)
    self.assertEqual(days, 0)
    self.assertEqual(hours, 5)
    self.assertEqual(minutes, 3)
    self.assertEqual(seconds, 10)

    days, hours, minutes, seconds = date_time_values._GetTimeValues(190990)
    self.assertEqual(days, 2)
    self.assertEqual(hours, 5)
    self.assertEqual(minutes, 3)
    self.assertEqual(seconds, 10)

    days, hours, minutes, seconds = date_time_values._GetTimeValues(-10)
    self.assertEqual(days, -1)
    self.assertEqual(hours, 23)
    self.assertEqual(minutes, 59)
    self.assertEqual(seconds, 50)

    days, hours, minutes, seconds = date_time_values._GetTimeValues(-190)
    self.assertEqual(days, -1)
    self.assertEqual(hours, 23)
    self.assertEqual(minutes, 56)
    self.assertEqual(seconds, 50)

    days, hours, minutes, seconds = date_time_values._GetTimeValues(-18190)
    self.assertEqual(days, -1)
    self.assertEqual(hours, 18)
    self.assertEqual(minutes, 56)
    self.assertEqual(seconds, 50)

    days, hours, minutes, seconds = date_time_values._GetTimeValues(-190990)
    self.assertEqual(days, -3)
    self.assertEqual(hours, 18)
    self.assertEqual(minutes, 56)
    self.assertEqual(seconds, 50)

  def testIsLeapYear(self):
    """Tests the _IsLeapYear function."""
    date_time_values = interface.DateTimeValues()

    self.assertFalse(date_time_values._IsLeapYear(1999))
    self.assertTrue(date_time_values._IsLeapYear(2000))
    self.assertTrue(date_time_values._IsLeapYear(1996))


if __name__ == '__main__':
  unittest.main()
