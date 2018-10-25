#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the time elements implementation."""

from __future__ import unicode_literals

import decimal
import unittest

from dfdatetime import time_elements


class TimeElementsTest(unittest.TestCase):
  """Tests for the time elements."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the initialization function."""
    time_elements_object = time_elements.TimeElements()
    self.assertIsNotNone(time_elements_object)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))
    self.assertIsNotNone(time_elements_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)

    with self.assertRaises(ValueError):
      time_elements.TimeElements(
          time_elements_tuple=(2010, 8, 12, 20, 6))

    with self.assertRaises(ValueError):
      time_elements.TimeElements(
          time_elements_tuple=(2010, 13, 12, 20, 6, 31))

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    normalized_timestamp = time_elements_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281643591'))

    time_elements_object = time_elements.TimeElements()

    normalized_timestamp = time_elements_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyDateTimeFromStringISO8601(self):
    """Tests the _CopyDateTimeFromStringISO8601 function."""
    time_elements_object = time_elements.TimeElements()

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12}
    date_dict = time_elements_object._CopyDateTimeFromStringISO8601(
        '2010-08-12')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12,
        'hours': 21, 'minutes': 6, 'seconds': 31}
    date_dict = time_elements_object._CopyDateTimeFromStringISO8601(
        '2010-08-12T21:06:31')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12,
        'hours': 21, 'minutes': 6, 'seconds': 31, 'microseconds': 546875}
    date_dict = time_elements_object._CopyDateTimeFromStringISO8601(
        '2010-08-12T21:06:31.546875')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12,
        'hours': 22, 'minutes': 6, 'seconds': 31, 'microseconds': 546875}
    date_dict = time_elements_object._CopyDateTimeFromStringISO8601(
        '2010-08-12T21:06:31.546875-01:00')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12,
        'hours': 20, 'minutes': 6, 'seconds': 31, 'microseconds': 546875}
    date_dict = time_elements_object._CopyDateTimeFromStringISO8601(
        '2010-08-12T21:06:31.546875+01:00')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12,
        'hours': 20, 'minutes': 6, 'seconds': 31, 'microseconds': 546875}
    date_dict = time_elements_object._CopyDateTimeFromStringISO8601(
        '2010-08-12T21:06:31.546875+01:00')
    self.assertEqual(date_dict, expected_date_dict)

    # Test backwards date correction.
    expected_date_dict = {
        'year': 2009, 'month': 12, 'day_of_month': 31,
        'hours': 23, 'minutes': 45, 'seconds': 0, 'microseconds': 123456}
    date_dict = time_elements_object._CopyDateTimeFromStringISO8601(
        '2010-01-01T00:15:00.123456+00:30')
    self.assertEqual(date_dict, expected_date_dict)

    # Test forward date correction.
    expected_date_dict = {
        'year': 2010, 'month': 1, 'day_of_month': 1,
        'hours': 1, 'minutes': 15, 'seconds': 0, 'microseconds': 123456}
    date_dict = time_elements_object._CopyDateTimeFromStringISO8601(
        '2009-12-31T23:45:00.123456-01:30')
    self.assertEqual(date_dict, expected_date_dict)

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringISO8601('')

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringISO8601('2010-08-12T1')

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringISO8601(
          '2010-08-12 21:06:31.546875+01:00')

  # TODO: add tests for _CopyFromDateTimeValues

  def testCopyTimeFromStringISO8601(self):
    """Tests the _CopyTimeFromStringISO8601 function."""
    time_elements_object = time_elements.TimeElements()

    expected_time_tuple = (8, None, None, None, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('08')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (8, 4, None, None, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('08:04')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (8, 4, None, None, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('0804')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 30, 0, 0, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('20.5')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (8, 4, 32, None, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('08:04:32')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (8, 4, 32, None, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('080432')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 30, 0, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('20:23.5')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 30, 0, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('2023.5')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (8, 4, 32, None, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('08:04:32Z')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, None, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('20:23:56')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, None, -330)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601(
        '20:23:56+05:30')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, 327000, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('20:23:56.327')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, 327000, -60)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601(
        '20:23:56.327+01:00')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, 327124, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601(
        '20:23:56.327124')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, 327124, 300)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601(
        '20:23:56.327124-05:00')
    self.assertEqual(time_tuple, expected_time_tuple)

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('1')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('14:1')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('14:15:1')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('24:00:00')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('12b00:00')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('12:00b00')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('1s:00:00')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('00:60:00')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('00:e0:00')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('00:00:60')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('00:00:w0')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('12:00:00.00w')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('12:00:00+01b00')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('12:00:00+0w:00')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('12:00:00+20:00')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('12:00:00+01:0w')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringISO8601('12:00:00+01:60')

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    time_elements_object = time_elements.TimeElements()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    expected_number_of_seconds = 1281571200
    time_elements_object.CopyFromString('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    time_elements_object = time_elements.TimeElements()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    expected_number_of_seconds = 1281571200
    time_elements_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 22, 6, 31)
    expected_number_of_seconds = 1281650791
    time_elements_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    expected_number_of_seconds = 1281643591
    time_elements_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (1601, 1, 2, 0, 0, 0)
    expected_number_of_seconds = -11644387200
    time_elements_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

  def testCopyFromStringISO8601(self):
    """Tests the CopyFromStringISO8601 function."""
    time_elements_object = time_elements.TimeElements()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    expected_number_of_seconds = 1281571200
    time_elements_object.CopyFromStringISO8601('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31Z')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31.5')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31,546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2012, 3, 5, 20, 40, 0)
    expected_number_of_seconds = 1330980000
    time_elements_object.CopyFromStringISO8601('2012-03-05T20:40:00.0000000Z')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 22, 6, 31)
    expected_number_of_seconds = 1281650791
    time_elements_object.CopyFromStringISO8601(
        '2010-08-12T21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    expected_number_of_seconds = 1281643591
    time_elements_object.CopyFromStringISO8601(
        '2010-08-12T21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(None)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(
          '2010-08-12 21:06:31.546875+01:00')

    # Valid ISO 8601 notations currently not supported.
    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601('2016-W33')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601('2016-W33-3')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601('--08-17')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601('2016-230')

  def testCopyFromStringTuple(self):
    """Tests the CopyFromStringTuple function."""
    time_elements_object = time_elements.TimeElements()

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    time_elements_object.CopyFromStringTuple(
        time_elements_tuple=('2010', '8', '12', '20', '6', '31'))
    self.assertIsNotNone(time_elements_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=('2010', '8', '12', '20', '6'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=('20A0', 'B', '12', '20', '6', '31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=('2010', 'B', '12', '20', '6', '31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=('2010', '8', '1C', '20', '6', '31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=('2010', '8', '12', 'D0', '6', '31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=('2010', '8', '12', '20', 'E', '31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=('2010', '8', '12', '20', '6', 'F1'))

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    date_time_string = time_elements_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31')

    time_elements_object = time_elements.TimeElements()

    date_time_string = time_elements_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    date_time_string = time_elements_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31Z')

  def testCopyToPosixTimestamp(self):
    """Tests the CopyToPosixTimestamp function."""
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    posix_timestamp = time_elements_object.CopyToPosixTimestamp()
    self.assertEqual(posix_timestamp, 1281643591)

    time_elements_object = time_elements.TimeElements()

    posix_timestamp = time_elements_object.CopyToPosixTimestamp()
    self.assertIsNone(posix_timestamp)

  def testGetDate(self):
    """Tests the GetDate function."""
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    date_tuple = time_elements_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    time_elements_object = time_elements.TimeElements()

    date_tuple = time_elements_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    time_of_day_tuple = time_elements_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (20, 6, 31))

    time_elements_object = time_elements.TimeElements()

    time_of_day_tuple = time_elements_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


class TimeElementsInMillisecondsTest(unittest.TestCase):
  """Tests for the time elements in milliseconds."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the initialization function."""
    time_elements_object = time_elements.TimeElements()
    self.assertIsNotNone(time_elements_object)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 546))
    self.assertIsNotNone(time_elements_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object.milliseconds, 546)

    with self.assertRaises(ValueError):
      time_elements.TimeElementsInMilliseconds(
          time_elements_tuple=(2010, 13, 12, 20, 6, 31))

    with self.assertRaises(ValueError):
      time_elements.TimeElementsInMilliseconds(
          time_elements_tuple=(2010, 13, 12, 20, 6, 31, 1001))

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429))

    normalized_timestamp = time_elements_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281643591.429'))

    time_elements_object = time_elements.TimeElementsInMilliseconds()

    normalized_timestamp = time_elements_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  # TODO: add tests for _CopyFromDateTimeValues

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    expected_number_of_seconds = 1281571200
    time_elements_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 546)

    expected_time_elements_tuple = (2010, 8, 12, 22, 6, 31)
    expected_number_of_seconds = 1281650791
    time_elements_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 546)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    expected_number_of_seconds = 1281643591
    time_elements_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 546)

    expected_time_elements_tuple = (1601, 1, 2, 0, 0, 0)
    expected_number_of_seconds = -11644387200
    time_elements_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 0)

  def testCopyFromStringISO8601(self):
    """Tests the CopyFromStringISO8601 function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    expected_number_of_seconds = 1281571200
    time_elements_object.CopyFromStringISO8601('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31Z')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31.5')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 500)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 546)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31,546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 546)

    expected_time_elements_tuple = (2012, 3, 5, 20, 40, 0)
    expected_number_of_seconds = 1330980000
    time_elements_object.CopyFromStringISO8601('2012-03-05T20:40:00.0000000Z')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 0)

    expected_time_elements_tuple = (2010, 8, 12, 22, 6, 31)
    expected_number_of_seconds = 1281650791
    time_elements_object.CopyFromStringISO8601(
        '2010-08-12T21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 546)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    expected_number_of_seconds = 1281643591
    time_elements_object.CopyFromStringISO8601(
        '2010-08-12T21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 546)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(None)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(
          '2010-08-12 21:06:31.546875+01:00')

    # Valid ISO 8601 notations currently not supported.
    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601('2016-W33')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601('2016-W33-3')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601('--08-17')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601('2016-230')

  def testCopyFromStringTuple(self):
    """Tests the CopyFromStringTuple function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds()

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    time_elements_object.CopyFromStringTuple(
        time_elements_tuple=('2010', '8', '12', '20', '6', '31', '546'))
    self.assertIsNotNone(time_elements_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object.milliseconds, 546)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=('2010', '8', '12', '20', '6', '31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=('2010', '8', '12', '20', '6', '31', '9S'))

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429))

    date_time_string = time_elements_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31.429')

    time_elements_object = time_elements.TimeElementsInMilliseconds()

    date_time_string = time_elements_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429))

    date_time_string = time_elements_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.429Z')

  def testGetDate(self):
    """Tests the GetDate function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429))

    date_tuple = time_elements_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    time_elements_object = time_elements.TimeElementsInMilliseconds()

    date_tuple = time_elements_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429))

    time_of_day_tuple = time_elements_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (20, 6, 31))

    time_elements_object = time_elements.TimeElementsInMilliseconds()

    time_of_day_tuple = time_elements_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


class TimeElementsInMicrosecondsTest(unittest.TestCase):
  """Tests for the time elements in microseconds."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the initialization function."""
    time_elements_object = time_elements.TimeElements()
    self.assertIsNotNone(time_elements_object)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    time_elements_object = time_elements.TimeElementsInMicroseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 546))
    self.assertIsNotNone(time_elements_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object.microseconds, 546)

    with self.assertRaises(ValueError):
      time_elements.TimeElementsInMicroseconds(
          time_elements_tuple=(2010, 13, 12, 20, 6, 31))

    with self.assertRaises(ValueError):
      time_elements.TimeElementsInMicroseconds(
          time_elements_tuple=(2010, 13, 12, 20, 6, 31, 1001))

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429876))

    normalized_timestamp = time_elements_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281643591.429876'))

    time_elements_object = time_elements.TimeElementsInMicroseconds()

    normalized_timestamp = time_elements_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  # TODO: add tests for _CopyFromDateTimeValues

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    expected_number_of_seconds = 1281571200
    time_elements_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 546875)

    expected_time_elements_tuple = (2010, 8, 12, 22, 6, 31)
    expected_number_of_seconds = 1281650791
    time_elements_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 546875)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    expected_number_of_seconds = 1281643591
    time_elements_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 546875)

    expected_time_elements_tuple = (1601, 1, 2, 0, 0, 0)
    expected_number_of_seconds = -11644387200
    time_elements_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 0)

  def testCopyFromStringISO8601(self):
    """Tests the CopyFromStringISO8601 function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    expected_number_of_seconds = 1281571200
    time_elements_object.CopyFromStringISO8601('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31Z')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31.5')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 500000)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 546875)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31,546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 546875)

    expected_time_elements_tuple = (2012, 3, 5, 20, 40, 0)
    expected_number_of_seconds = 1330980000
    time_elements_object.CopyFromStringISO8601('2012-03-05T20:40:00.0000000Z')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 0)

    expected_time_elements_tuple = (2010, 8, 12, 22, 6, 31)
    expected_number_of_seconds = 1281650791
    time_elements_object.CopyFromStringISO8601(
        '2010-08-12T21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 546875)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    expected_number_of_seconds = 1281643591
    time_elements_object.CopyFromStringISO8601(
        '2010-08-12T21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 546875)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(None)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(
          '2010-08-12 21:06:31.546875+01:00')

    # Valid ISO 8601 notations currently not supported.
    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601('2016-W33')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601('2016-W33-3')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601('--08-17')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601('2016-230')

  def testCopyFromStringTuple(self):
    """Tests the CopyFromStringTuple function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds()

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    time_elements_object.CopyFromStringTuple(
        time_elements_tuple=('2010', '8', '12', '20', '6', '31', '546'))
    self.assertIsNotNone(time_elements_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object.microseconds, 546)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=('2010', '8', '12', '20', '6', '31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=('2010', '8', '12', '20', '6', '31', '9S'))

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429876))

    date_time_string = time_elements_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31.429876')

    time_elements_object = time_elements.TimeElementsInMicroseconds()

    date_time_string = time_elements_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429876))

    date_time_string = time_elements_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.429876Z')

  def testGetDate(self):
    """Tests the GetDate function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429876))

    date_tuple = time_elements_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    time_elements_object = time_elements.TimeElementsInMicroseconds()

    date_tuple = time_elements_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429876))

    time_of_day_tuple = time_elements_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (20, 6, 31))

    time_elements_object = time_elements.TimeElementsInMicroseconds()

    time_of_day_tuple = time_elements_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
