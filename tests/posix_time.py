#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the POSIX time implementation."""

import decimal
import unittest

from dfdatetime import posix_time


class PosixTimeEpochTest(unittest.TestCase):
  """Tests for the POSIX time epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    posix_epoch = posix_time.PosixTimeEpoch()
    self.assertIsNotNone(posix_epoch)


class PosixTimeTest(unittest.TestCase):
  """Tests for the POSIX timestamp."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the properties."""
    posix_time_object = posix_time.PosixTime(timestamp=1281643591)
    self.assertEqual(posix_time_object.timestamp, 1281643591)

    posix_time_object = posix_time.PosixTime()
    self.assertIsNone(posix_time_object.timestamp)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    posix_time_object = posix_time.PosixTime(timestamp=1281643591)

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281643591.0'))

    posix_time_object = posix_time.PosixTime(
        time_zone_offset=60, timestamp=1281643591)

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281639991.0'))

    posix_time_object = posix_time.PosixTime()

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    posix_time_object = posix_time.PosixTime()

    posix_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(posix_time_object._timestamp, 1281571200)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(posix_time_object._timestamp, 1281647191)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(posix_time_object._timestamp, 1281647191)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(posix_time_object._timestamp, 1281647191)
    self.assertEqual(posix_time_object._time_zone_offset, -60)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(posix_time_object._timestamp, 1281647191)
    self.assertEqual(posix_time_object._time_zone_offset, 60)

    posix_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(posix_time_object._timestamp, -11644387200)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    posix_time_object = posix_time.PosixTime(timestamp=1281643591)

    date_time_string = posix_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31')

    posix_time_object = posix_time.PosixTime()

    date_time_string = posix_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    posix_time_object = posix_time.PosixTime(timestamp=1281643591)

    date_time_string = posix_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31+00:00')

    posix_time_object = posix_time.PosixTime(timestamp=-11644468446)

    date_time_string = posix_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '1601-01-01T01:25:54+00:00')

  def testCopyToPosixTimestampWithFractionOfSecond(self):
    """Tests the CopyToPosixTimestampWithFractionOfSecond function."""
    posix_time_object = posix_time.PosixTime(timestamp=1281643591)

    posix_timestamp, fraction_of_second = (
        posix_time_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertEqual(posix_timestamp, 1281643591)
    self.assertIsNone(fraction_of_second)

    posix_time_object = posix_time.PosixTime(timestamp=-11644468446)

    posix_timestamp, fraction_of_second = (
        posix_time_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertEqual(posix_timestamp, -11644468446)
    self.assertIsNone(fraction_of_second)

    posix_time_object = posix_time.PosixTime()

    posix_timestamp, fraction_of_second = (
        posix_time_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertIsNone(posix_timestamp)
    self.assertIsNone(fraction_of_second)

  def testGetDate(self):
    """Tests the GetDate function."""
    posix_time_object = posix_time.PosixTime(timestamp=1281643591)

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    posix_time_object = posix_time.PosixTime()

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    posix_time_object = posix_time.PosixTime(timestamp=1281643591)

    date_with_time_of_day_tuple = posix_time_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2010, 8, 12, 20, 6, 31))

    posix_time_object = posix_time.PosixTime()

    date_with_time_of_day_tuple = posix_time_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    posix_time_object = posix_time.PosixTime(timestamp=1281643591)

    time_of_day_tuple = posix_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (20, 6, 31))

    posix_time_object = posix_time.PosixTime()

    time_of_day_tuple = posix_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


class PosixTimeInMillisecondsTest(unittest.TestCase):
  """Tests for the POSIX timestamp in milliseconds."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the properties."""
    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=1281643591546)
    self.assertEqual(posix_time_object.timestamp, 1281643591546)

    posix_time_object = posix_time.PosixTimeInMilliseconds()
    self.assertIsNone(posix_time_object.timestamp)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=1281643591546)

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281643591.546'))

    posix_time_object = posix_time.PosixTimeInMilliseconds(
        time_zone_offset=60, timestamp=1281643591546)

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281639991.546'))

    posix_time_object = posix_time.PosixTimeInMilliseconds()

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  # pylint: disable=protected-access

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    posix_time_object = posix_time.PosixTimeInMilliseconds()

    posix_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(posix_time_object._timestamp, 1281571200000)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(posix_time_object._timestamp, 1281647191000)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546')
    self.assertEqual(posix_time_object._timestamp, 1281647191546)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546-01:00')
    self.assertEqual(posix_time_object._timestamp, 1281647191546)
    self.assertEqual(posix_time_object._time_zone_offset, -60)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546+01:00')
    self.assertEqual(posix_time_object._timestamp, 1281647191546)
    self.assertEqual(posix_time_object._time_zone_offset, 60)

    posix_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(posix_time_object._timestamp, -11644387200000)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=1281643591546)

    date_time_string = posix_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31.546')

    posix_time_object = posix_time.PosixTimeInMilliseconds()

    date_time_string = posix_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=1281643591546)

    date_time_string = posix_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.546+00:00')

    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=-11644468446327)

    date_time_string = posix_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '1601-01-01T01:25:53.673+00:00')

  def testCopyToPosixTimestampWithFractionOfSecond(self):
    """Tests the CopyToPosixTimestampWithFractionOfSecond function."""
    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=1281643591546)

    posix_timestamp, fraction_of_second = (
        posix_time_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertEqual(posix_timestamp, 1281643591)
    self.assertEqual(fraction_of_second, 546)

    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=-11644468446327)

    posix_timestamp, fraction_of_second = (
        posix_time_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertEqual(posix_timestamp, -11644468446)
    self.assertEqual(fraction_of_second, -327)

    posix_time_object = posix_time.PosixTime()

    posix_timestamp, fraction_of_second = (
        posix_time_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertIsNone(posix_timestamp)
    self.assertIsNone(fraction_of_second)

  def testGetDate(self):
    """Tests the GetDate function."""
    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=1281643591546)

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    posix_time_object = posix_time.PosixTimeInMilliseconds()

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=1281643591546)

    date_with_time_of_day_tuple = posix_time_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2010, 8, 12, 20, 6, 31))

    posix_time_object = posix_time.PosixTimeInMilliseconds()

    date_with_time_of_day_tuple = posix_time_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=1281643591546)

    time_of_day_tuple = posix_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (20, 6, 31))

    posix_time_object = posix_time.PosixTimeInMilliseconds()

    time_of_day_tuple = posix_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


class PosixTimeInMicrosecondsTest(unittest.TestCase):
  """Tests for the POSIX timestamp in microseconds."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the properties."""
    posix_time_object = posix_time.PosixTimeInMicroseconds(
        timestamp=1281643591546875)
    self.assertEqual(posix_time_object.timestamp, 1281643591546875)

    posix_time_object = posix_time.PosixTimeInMicroseconds()
    self.assertIsNone(posix_time_object.timestamp)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=1281643591546)

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281643591.546'))

    posix_time_object = posix_time.PosixTimeInMicroseconds(
        time_zone_offset=60, timestamp=1281643591546875)

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281639991.546875'))

    posix_time_object = posix_time.PosixTimeInMicroseconds()

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  # pylint: disable=protected-access

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    posix_time_object = posix_time.PosixTimeInMicroseconds()

    posix_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(posix_time_object._timestamp, 1281571200000000)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(posix_time_object._timestamp, 1281647191000000)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(posix_time_object._timestamp, 1281647191546875)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(posix_time_object._timestamp, 1281647191546875)
    self.assertEqual(posix_time_object._time_zone_offset, -60)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(posix_time_object._timestamp, 1281647191546875)
    self.assertEqual(posix_time_object._time_zone_offset, 60)

    posix_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(posix_time_object._timestamp, -11644387200000000)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    posix_time_object = posix_time.PosixTimeInMicroseconds(
        timestamp=1281643591546875)

    date_time_string = posix_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31.546875')

    posix_time_object = posix_time.PosixTimeInMicroseconds()

    date_time_string = posix_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    posix_time_object = posix_time.PosixTimeInMicroseconds(
        timestamp=1281643591546875)

    date_time_string = posix_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.546875+00:00')

    posix_time_object = posix_time.PosixTimeInMicroseconds(
        timestamp=-11644468446327447)

    date_time_string = posix_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '1601-01-01T01:25:53.672553+00:00')

  def testCopyToPosixTimestampWithFractionOfSecond(self):
    """Tests the CopyToPosixTimestampWithFractionOfSecond function."""
    posix_time_object = posix_time.PosixTimeInMicroseconds(
        timestamp=1281643591546875)

    posix_timestamp, fraction_of_second = (
        posix_time_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertEqual(posix_timestamp, 1281643591)
    self.assertEqual(fraction_of_second, 546875)

    posix_time_object = posix_time.PosixTimeInMicroseconds(
        timestamp=-11644468446327447)

    posix_timestamp, fraction_of_second = (
        posix_time_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertEqual(posix_timestamp, -11644468446)
    self.assertEqual(fraction_of_second, -327447)

    posix_time_object = posix_time.PosixTime()

    posix_timestamp, fraction_of_second = (
        posix_time_object.CopyToPosixTimestampWithFractionOfSecond())
    self.assertIsNone(posix_timestamp)
    self.assertIsNone(fraction_of_second)

  def testGetDate(self):
    """Tests the GetDate function."""
    posix_time_object = posix_time.PosixTimeInMicroseconds(
        timestamp=1281643591546875)

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    posix_time_object = posix_time.PosixTimeInMicroseconds()

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    posix_time_object = posix_time.PosixTimeInMicroseconds(
        timestamp=1281643591546875)

    date_with_time_of_day_tuple = posix_time_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2010, 8, 12, 20, 6, 31))

    posix_time_object = posix_time.PosixTimeInMicroseconds()

    date_with_time_of_day_tuple = posix_time_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    posix_time_object = posix_time.PosixTimeInMicroseconds(
        timestamp=1281643591546875)

    time_of_day_tuple = posix_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (20, 6, 31))

    posix_time_object = posix_time.PosixTimeInMicroseconds()

    time_of_day_tuple = posix_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


class PosixTimeInNanoSecondsTest(unittest.TestCase):
  """Tests for the POSIX timestamp in nanoseconds."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the properties."""
    posix_time_object = posix_time.PosixTimeInNanoseconds(
        timestamp=1281643591987654321)
    self.assertEqual(posix_time_object.timestamp, 1281643591987654321)

    posix_time_object = posix_time.PosixTimeInNanoseconds()
    self.assertIsNone(posix_time_object.timestamp)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    posix_time_object = posix_time.PosixTimeInNanoseconds(
        timestamp=1281643591987654321)

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertEqual(
        normalized_timestamp, decimal.Decimal('1281643591.987654321'))

    posix_time_object = posix_time.PosixTimeInNanoseconds(
        time_zone_offset=60, timestamp=1281643591987654321)

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertEqual(
        normalized_timestamp, decimal.Decimal('1281639991.987654321'))

    posix_time_object = posix_time.PosixTimeInNanoseconds()

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    posix_time_object = posix_time.PosixTimeInNanoseconds()

    posix_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(posix_time_object.timestamp, 1281571200000000000)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(posix_time_object.timestamp, 1281647191000000000)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.654321')
    self.assertEqual(posix_time_object.timestamp, 1281647191654321000)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

    posix_time_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.654321-01:00')
    self.assertEqual(posix_time_object.timestamp, 1281647191654321000)
    self.assertEqual(posix_time_object._time_zone_offset, -60)

    posix_time_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.654321+01:00')
    self.assertEqual(posix_time_object.timestamp, 1281647191654321000)
    self.assertEqual(posix_time_object._time_zone_offset, 60)

    posix_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(posix_time_object.timestamp, -11644387200000000000)
    self.assertEqual(posix_time_object._time_zone_offset, 0)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    posix_time_object = posix_time.PosixTimeInNanoseconds(
        timestamp=1281643591987654321)

    date_time_string = posix_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31.987654321')

    posix_time_object = posix_time.PosixTimeInNanoseconds()

    date_time_string = posix_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    posix_time_object = posix_time.PosixTimeInNanoseconds(
        timestamp=1281643591987654321)

    date_time_string = posix_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.987654321+00:00')

  def testGetDate(self):
    """Tests the GetDate function."""
    posix_time_object = posix_time.PosixTimeInNanoseconds(
        timestamp=1281643591987654321)

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    posix_time_object = posix_time.PosixTimeInNanoseconds()

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    posix_time_object = posix_time.PosixTimeInNanoseconds(
        timestamp=1281643591987654321)

    date_with_time_of_day_tuple = posix_time_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2010, 8, 12, 20, 6, 31))

    posix_time_object = posix_time.PosixTimeInNanoseconds()

    date_with_time_of_day_tuple = posix_time_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    posix_time_object = posix_time.PosixTimeInNanoseconds(
        timestamp=1281643591987654321)

    time_of_day_tuple = posix_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (20, 6, 31))

    posix_time_object = posix_time.PosixTimeInNanoseconds()

    time_of_day_tuple = posix_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
