#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the time elements implementation."""

import datetime
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
    self.assertEqual(time_elements_object.year, 2010)
    self.assertEqual(time_elements_object.month, 8)
    self.assertEqual(time_elements_object.day_of_month, 12)
    self.assertEqual(time_elements_object.hours, 20)
    self.assertEqual(time_elements_object.minutes, 6)
    self.assertEqual(time_elements_object.seconds, 31)

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

    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31), time_zone_offset=60)

    normalized_timestamp = time_elements_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281639991'))

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
        'hours': 21, 'minutes': 6, 'seconds': 31, 'microseconds': 546875,
        'time_zone_offset': -60}
    date_dict = time_elements_object._CopyDateTimeFromStringISO8601(
        '2010-08-12T21:06:31.546875-01:00')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 2010, 'month': 8, 'day_of_month': 12,
        'hours': 21, 'minutes': 6, 'seconds': 31, 'microseconds': 546875,
        'time_zone_offset': 60}
    date_dict = time_elements_object._CopyDateTimeFromStringISO8601(
        '2010-08-12T21:06:31.546875+01:00')
    self.assertEqual(date_dict, expected_date_dict)

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringISO8601('')

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringISO8601('2010-08-12T1')

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringISO8601(
          '2010-08-12 21:06:31.546875+01:00')

  def testCopyDateTimeFromStringRFC822(self):
    """Tests the _CopyDateTimeFromStringRFC822 function."""
    time_elements_object = time_elements.TimeElements()

    expected_date_dict = {
        'year': 1982, 'month': 6, 'day_of_month': 20,
        'hours': 11, 'minutes': 57, 'seconds': 9,
        'time_zone_offset': 0}
    date_dict = time_elements_object._CopyDateTimeFromStringRFC822(
        'Sun, 20 Jun 82 11:57:09 GMT')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 1982, 'month': 6, 'day_of_month': 20,
        'hours': 11, 'minutes': 57, 'seconds': 9,
        'time_zone_offset': 0}
    date_dict = time_elements_object._CopyDateTimeFromStringRFC822(
        '20 Jun 82 11:57:09 GMT')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 1982, 'month': 6, 'day_of_month': 20,
        'hours': 11, 'minutes': 57,
        'time_zone_offset': 0}
    date_dict = time_elements_object._CopyDateTimeFromStringRFC822(
        '20 Jun 82 11:57 GMT')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 1982, 'month': 6, 'day_of_month': 20,
        'hours': 11, 'minutes': 57, 'seconds': 9,
        'time_zone_offset': -300}
    date_dict = time_elements_object._CopyDateTimeFromStringRFC822(
        'Sun, 20 Jun 82 11:57:09 EST')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 1982, 'month': 6, 'day_of_month': 20,
        'hours': 11, 'minutes': 57, 'seconds': 9,
        'time_zone_offset': -300}
    date_dict = time_elements_object._CopyDateTimeFromStringRFC822(
        'Sun, 20 Jun 82 11:57:09 -0500')
    self.assertEqual(date_dict, expected_date_dict)

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringRFC822(
          'XXX, 20 Jun 82 11:57:09 GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringRFC822(
          'Sun, XX Jun 82 11:57:09 GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringRFC822(
          'Sun, 20 XXX 82 11:57:09 GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringRFC822(
          'Sun, 20 Jun XX 11:57:09 GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringRFC822(
          'Sun, 20 Jun 82 XX:XX:XX XXX')

  def testCopyDateTimeFromStringRFC1123(self):
    """Tests the _CopyDateTimeFromStringRFC1123 function."""
    time_elements_object = time_elements.TimeElements()

    expected_date_dict = {
        'year': 1982, 'month': 6, 'day_of_month': 20,
        'hours': 11, 'minutes': 57, 'seconds': 9,
        'time_zone_offset': 0}
    date_dict = time_elements_object._CopyDateTimeFromStringRFC1123(
        'Sun, 20 Jun 1982 11:57:09 GMT')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 1982, 'month': 6, 'day_of_month': 20,
        'hours': 11, 'minutes': 57, 'seconds': 9,
        'time_zone_offset': 0}
    date_dict = time_elements_object._CopyDateTimeFromStringRFC1123(
        '20 Jun 1982 11:57:09 GMT')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 1982, 'month': 6, 'day_of_month': 20,
        'hours': 11, 'minutes': 57,
        'time_zone_offset': 0}
    date_dict = time_elements_object._CopyDateTimeFromStringRFC1123(
        '20 Jun 1982 11:57 GMT')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 1982, 'month': 6, 'day_of_month': 20,
        'hours': 11, 'minutes': 57, 'seconds': 9,
        'time_zone_offset': -300}
    date_dict = time_elements_object._CopyDateTimeFromStringRFC1123(
        'Sun, 20 Jun 1982 11:57:09 EST')
    self.assertEqual(date_dict, expected_date_dict)

    expected_date_dict = {
        'year': 1982, 'month': 6, 'day_of_month': 20,
        'hours': 11, 'minutes': 57, 'seconds': 9,
        'time_zone_offset': -300}
    date_dict = time_elements_object._CopyDateTimeFromStringRFC1123(
        'Sun, 20 Jun 1982 11:57:09 -0500')
    self.assertEqual(date_dict, expected_date_dict)

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringRFC1123(
          'XXX, 20 Jun 1982 11:57:09 GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringRFC1123(
          'Sun, XX Jun 1982 11:57:09 GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringRFC1123(
          'Sun, 20 XXX 1982 11:57:09 GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringRFC1123(
          'Sun, 20 Jun XXXX 11:57:09 GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyDateTimeFromStringRFC1123(
          'Sun, 20 Jun 1982 XX:XX:XX XXX')

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

    expected_time_tuple = (20, 23, 56, None, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('20:23:56')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, None, 330)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601(
        '20:23:56+05:30')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, 327000, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('20:23:56.327')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, 327000, 60)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601(
        '20:23:56.327+01:00')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, 327124, None)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601(
        '20:23:56.327124')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (8, 4, 32, None, 0)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601('08:04:32Z')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (8, 4, 32, None, 0)
    time_tuple = time_elements_object._CopyTimeFromStringISO8601(
        '08:04:32+00:00')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (20, 23, 56, 327124, -300)
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

  def testCopyTimeFromStringRFC(self):
    """Tests the _CopyTimeFromStringRFC function."""
    time_elements_object = time_elements.TimeElements()

    expected_time_tuple = (11, 57, 9, 0)
    time_tuple = time_elements_object._CopyTimeFromStringRFC('11:57:09', 'GMT')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (11, 57, None, 0)
    time_tuple = time_elements_object._CopyTimeFromStringRFC('11:57', 'GMT')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (11, 57, None, -300)
    time_tuple = time_elements_object._CopyTimeFromStringRFC('11:57', 'EST')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (11, 57, None, -300)
    time_tuple = time_elements_object._CopyTimeFromStringRFC('11:57', '-0500')
    self.assertEqual(time_tuple, expected_time_tuple)

    expected_time_tuple = (11, 57, None, 60)
    time_tuple = time_elements_object._CopyTimeFromStringRFC('11:57', '+0100')
    self.assertEqual(time_tuple, expected_time_tuple)

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringRFC('11:', 'GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringRFC('11:57:', 'GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringRFC('XX:57:09', 'GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringRFC('24:57:09', 'GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringRFC('11:XX:09', 'GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringRFC('11:60:09', 'GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringRFC('11:57:XX', 'GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringRFC('11:57:60', 'GMT')

    with self.assertRaises(ValueError):
      time_elements_object._CopyTimeFromStringRFC('11:57:09', 'XXX')

  def testCopyFromDatetime(self):
    """Tests the CopyFromDatetime function."""
    time_elements_object = time_elements.TimeElements()

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191

    datetime_object = datetime.datetime(2010, 8, 12, 21, 6, 31, 546875)
    time_elements_object.CopyFromDatetime(datetime_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertTrue(time_elements_object.is_local_time)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191

    datetime_object = datetime.datetime(
        2010, 8, 12, 21, 6, 31, 546875, tzinfo=datetime.timezone.utc)
    time_elements_object.CopyFromDatetime(datetime_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertFalse(time_elements_object.is_local_time)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    time_elements_object = time_elements.TimeElements()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    time_elements_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281571200)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object._time_zone_offset, -60)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object._time_zone_offset, 60)

    expected_time_elements_tuple = (1601, 1, 2, 0, 0, 0)
    time_elements_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, -11644387200)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

  def testCopyFromStringISO8601(self):
    """Tests the CopyFromStringISO8601 function."""
    time_elements_object = time_elements.TimeElements()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    time_elements_object.CopyFromStringISO8601('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281571200)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31+00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31.5')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31,546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601(
        '2010-08-12T21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object._time_zone_offset, -60)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601(
        '2010-08-12T21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object._time_zone_offset, 60)

    expected_time_elements_tuple = (2012, 3, 5, 20, 40, 0)
    time_elements_object.CopyFromStringISO8601(
        '2012-03-05T20:40:00.0000000+00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1330980000)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

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
    self.assertEqual(date_time_string, '2010-08-12T20:06:31+00:00')

    time_elements_object.is_local_time = True

    date_time_string = time_elements_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31')

    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31),
        time_zone_offset=120)

    date_time_string = time_elements_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31+02:00')

    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31),
        time_zone_offset=-300)

    date_time_string = time_elements_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31-05:00')

  def testCopyToPosixTimestamp(self):
    """Tests the CopyToPosixTimestamp function."""
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    posix_timestamp = time_elements_object.CopyToPosixTimestamp()
    self.assertEqual(posix_timestamp, 1281643591)

    time_elements_object = time_elements.TimeElements()

    posix_timestamp = time_elements_object.CopyToPosixTimestamp()
    self.assertIsNone(posix_timestamp)

  def testCopyToPosixTimestampWithFractionOfSecond(self):
    """Tests the CopyToPosixTimestampWithFractionOfSecond function."""
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    posix_timestamp, fraction_of_second = (
        time_elements_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertEqual(posix_timestamp, 1281643591)
    self.assertIsNone(fraction_of_second)

    time_elements_object = time_elements.TimeElements()

    posix_timestamp, fraction_of_second = (
        time_elements_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertIsNone(posix_timestamp)
    self.assertIsNone(fraction_of_second)

  def testGetDate(self):
    """Tests the GetDate function."""
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    date_tuple = time_elements_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    time_elements_object = time_elements.TimeElements()

    date_tuple = time_elements_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    date_with_time_of_day_tuple = time_elements_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2010, 8, 12, 20, 6, 31))

    time_elements_object = time_elements.TimeElements()

    date_with_time_of_day_tuple = time_elements_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

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

    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429), time_zone_offset=60)

    normalized_timestamp = time_elements_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281639991.429'))

    time_elements_object = time_elements.TimeElementsInMilliseconds()

    normalized_timestamp = time_elements_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  # TODO: add tests for _CopyFromDateTimeValues

  def testCopyFromDatetime(self):
    """Tests the CopyFromDatetime function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds()

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191

    datetime_object = datetime.datetime(2010, 8, 12, 21, 6, 31, 546875)
    time_elements_object.CopyFromDatetime(datetime_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 546)
    self.assertTrue(time_elements_object.is_local_time)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191

    datetime_object = datetime.datetime(
        2010, 8, 12, 21, 6, 31, 546875, tzinfo=datetime.timezone.utc)
    time_elements_object.CopyFromDatetime(datetime_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.milliseconds, 546)
    self.assertFalse(time_elements_object.is_local_time)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    time_elements_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281571200)
    self.assertEqual(time_elements_object.milliseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.milliseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.milliseconds, 546)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.milliseconds, 546)
    self.assertEqual(time_elements_object._time_zone_offset, -60)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.milliseconds, 546)
    self.assertEqual(time_elements_object._time_zone_offset, 60)

    expected_time_elements_tuple = (1601, 1, 2, 0, 0, 0)
    time_elements_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, -11644387200)
    self.assertEqual(time_elements_object.milliseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

  def testCopyFromStringISO8601(self):
    """Tests the CopyFromStringISO8601 function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    time_elements_object.CopyFromStringISO8601('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281571200)
    self.assertEqual(time_elements_object.milliseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.milliseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31+00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.milliseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31.5')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.milliseconds, 500)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.milliseconds, 546)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31,546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.milliseconds, 546)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601(
        '2010-08-12T21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.milliseconds, 546)
    self.assertEqual(time_elements_object._time_zone_offset, -60)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601(
        '2010-08-12T21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.milliseconds, 546)
    self.assertEqual(time_elements_object._time_zone_offset, 60)

    expected_time_elements_tuple = (2012, 3, 5, 20, 40, 0)
    time_elements_object.CopyFromStringISO8601(
        '2012-03-05T20:40:00.0000000+00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1330980000)
    self.assertEqual(time_elements_object.milliseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

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
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.429+00:00')

  def testCopyToPosixTimestamp(self):
    """Tests the CopyToPosixTimestamp function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429))

    posix_timestamp = time_elements_object.CopyToPosixTimestamp()
    self.assertEqual(posix_timestamp, 1281643591)

    time_elements_object = time_elements.TimeElements()

    posix_timestamp = time_elements_object.CopyToPosixTimestamp()
    self.assertIsNone(posix_timestamp)

  def testCopyToPosixTimestampWithFractionOfSecond(self):
    """Tests the CopyToPosixTimestampWithFractionOfSecond function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429))

    posix_timestamp, fraction_of_second = (
        time_elements_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertEqual(posix_timestamp, 1281643591)
    self.assertEqual(fraction_of_second, 429)

    time_elements_object = time_elements.TimeElements()

    posix_timestamp, fraction_of_second = (
        time_elements_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertIsNone(posix_timestamp)
    self.assertIsNone(fraction_of_second)

  def testGetDate(self):
    """Tests the GetDate function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429))

    date_tuple = time_elements_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    time_elements_object = time_elements.TimeElementsInMilliseconds()

    date_tuple = time_elements_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429))

    date_with_time_of_day_tuple = time_elements_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2010, 8, 12, 20, 6, 31))

    time_elements_object = time_elements.TimeElementsInMilliseconds()

    date_with_time_of_day_tuple = time_elements_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

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

    time_elements_object = time_elements.TimeElementsInMicroseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429876),
        time_zone_offset=60)

    normalized_timestamp = time_elements_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281639991.429876'))

    time_elements_object = time_elements.TimeElementsInMicroseconds()

    normalized_timestamp = time_elements_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  # TODO: add tests for _CopyFromDateTimeValues

  def testCopyFromDatetime(self):
    """Tests the CopyFromDatetime function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds()

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191

    datetime_object = datetime.datetime(2010, 8, 12, 21, 6, 31, 546875)
    time_elements_object.CopyFromDatetime(datetime_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 546875)
    self.assertTrue(time_elements_object.is_local_time)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191

    datetime_object = datetime.datetime(
        2010, 8, 12, 21, 6, 31, 546875, tzinfo=datetime.timezone.utc)
    time_elements_object.CopyFromDatetime(datetime_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(time_elements_object.microseconds, 546875)
    self.assertFalse(time_elements_object.is_local_time)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    time_elements_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281571200)
    self.assertEqual(time_elements_object.microseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.microseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.microseconds, 546875)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.microseconds, 546875)
    self.assertEqual(time_elements_object._time_zone_offset, -60)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.microseconds, 546875)
    self.assertEqual(time_elements_object._time_zone_offset, 60)

    expected_time_elements_tuple = (1601, 1, 2, 0, 0, 0)
    time_elements_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, -11644387200)
    self.assertEqual(time_elements_object.microseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

  def testCopyFromStringISO8601(self):
    """Tests the CopyFromStringISO8601 function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    time_elements_object.CopyFromStringISO8601('2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281571200)
    self.assertEqual(time_elements_object.microseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.microseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31+00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.microseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31.5')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.microseconds, 500000)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.microseconds, 546875)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601('2010-08-12T21:06:31,546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.microseconds, 546875)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601(
        '2010-08-12T21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.microseconds, 546875)
    self.assertEqual(time_elements_object._time_zone_offset, -60)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    time_elements_object.CopyFromStringISO8601(
        '2010-08-12T21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1281647191)
    self.assertEqual(time_elements_object.microseconds, 546875)
    self.assertEqual(time_elements_object._time_zone_offset, 60)

    expected_time_elements_tuple = (2012, 3, 5, 20, 40, 0)
    time_elements_object.CopyFromStringISO8601(
        '2012-03-05T20:40:00.0000000+00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._number_of_seconds, 1330980000)
    self.assertEqual(time_elements_object.microseconds, 0)
    self.assertEqual(time_elements_object._time_zone_offset, 0)

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
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.429876+00:00')

  def testCopyToPosixTimestamp(self):
    """Tests the CopyToPosixTimestamp function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429876))

    posix_timestamp = time_elements_object.CopyToPosixTimestamp()
    self.assertEqual(posix_timestamp, 1281643591)

    time_elements_object = time_elements.TimeElements()

    posix_timestamp = time_elements_object.CopyToPosixTimestamp()
    self.assertIsNone(posix_timestamp)

  def testCopyToPosixTimestampWithFractionOfSecond(self):
    """Tests the CopyToPosixTimestampWithFractionOfSecond function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429876))

    posix_timestamp, fraction_of_second = (
        time_elements_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertEqual(posix_timestamp, 1281643591)
    self.assertEqual(fraction_of_second, 429876)

    time_elements_object = time_elements.TimeElements()

    posix_timestamp, fraction_of_second = (
        time_elements_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertIsNone(posix_timestamp)
    self.assertIsNone(fraction_of_second)

  def testGetDate(self):
    """Tests the GetDate function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429876))

    date_tuple = time_elements_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    time_elements_object = time_elements.TimeElementsInMicroseconds()

    date_tuple = time_elements_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    time_elements_object = time_elements.TimeElementsInMicroseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429876))

    date_with_time_of_day_tuple = time_elements_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2010, 8, 12, 20, 6, 31))

    time_elements_object = time_elements.TimeElementsInMicroseconds()

    date_with_time_of_day_tuple = time_elements_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

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
