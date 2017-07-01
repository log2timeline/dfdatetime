#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the date and time values interface."""

from __future__ import unicode_literals

import unittest

from dfdatetime import interface


class DateTimeValuesTest(unittest.TestCase):
  """Tests for the date and time values interface."""

  # pylint: disable=protected-access

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

  def testIsLeapYear(self):
    """Tests the _IsLeapYear function."""
    date_time_values = interface.DateTimeValues()

    self.assertFalse(date_time_values._IsLeapYear(1999))
    self.assertTrue(date_time_values._IsLeapYear(2000))
    self.assertTrue(date_time_values._IsLeapYear(1996))


if __name__ == '__main__':
  unittest.main()
