#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the POSIX time implementation."""

from __future__ import unicode_literals

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

    posix_time_object = posix_time.PosixTime()

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    posix_time_object = posix_time.PosixTime()

    expected_timestamp = 1281571200
    posix_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281650791
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281643591
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = -11644387200
    posix_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

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
    self.assertEqual(date_time_string, '2010-08-12T20:06:31Z')

  # TODO: remove this method when there is no more need for it in dfvfs.
  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    posix_time_object = posix_time.PosixTime(timestamp=1281643591)

    stat_time_tuple = posix_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (1281643591, None))

    posix_time_object = posix_time.PosixTime()

    stat_time_tuple = posix_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

  def testGetDate(self):
    """Tests the GetDate function."""
    posix_time_object = posix_time.PosixTime(timestamp=1281643591)

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    posix_time_object = posix_time.PosixTime()

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

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

    posix_time_object = posix_time.PosixTimeInMilliseconds()

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  # pylint: disable=protected-access

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    posix_time_object = posix_time.PosixTimeInMilliseconds()

    expected_timestamp = 1281571200000
    posix_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191000
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191546
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281650791546
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546-01:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281643591546
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546+01:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = -11644387200000
    posix_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

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
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.546Z')

  # TODO: remove this method when there is no more need for it in dfvfs.
  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=1281643591546)

    stat_time_tuple = posix_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (1281643591, 5460000))

    posix_time_object = posix_time.PosixTimeInMilliseconds()

    stat_time_tuple = posix_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

  def testGetDate(self):
    """Tests the GetDate function."""
    posix_time_object = posix_time.PosixTimeInMilliseconds(
        timestamp=1281643591546)

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    posix_time_object = posix_time.PosixTimeInMilliseconds()

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

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
    posix_time_object = posix_time.PosixTimeInMicroseconds(
        timestamp=1281643591546875)

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281643591.546875'))

    posix_time_object = posix_time.PosixTimeInMicroseconds()

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  # pylint: disable=protected-access

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    posix_time_object = posix_time.PosixTimeInMicroseconds()

    expected_timestamp = 1281571200000000
    posix_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191000000
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191546875
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281650791546875
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281643591546875
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = -11644387200000000
    posix_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

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
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.546875Z')

  # TODO: remove this method when there is no more need for it in dfvfs.
  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    posix_time_object = posix_time.PosixTimeInMicroseconds(
        timestamp=1281643591546875)

    stat_time_tuple = posix_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (1281643591, 5468750))

    posix_time_object = posix_time.PosixTimeInMicroseconds()

    stat_time_tuple = posix_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

  def testGetDate(self):
    """Tests the GetDate function."""
    posix_time_object = posix_time.PosixTimeInMicroseconds(
        timestamp=1281643591546875)

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    posix_time_object = posix_time.PosixTimeInMicroseconds()

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

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

    posix_time_object = posix_time.PosixTimeInNanoseconds()

    normalized_timestamp = posix_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    posix_time_object = posix_time.PosixTimeInNanoseconds()

    expected_timestamp = 1281571200000000000
    posix_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191000000000
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191654321000
    posix_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.654321')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281650791654321000
    posix_time_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.654321-01:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281643591654321000
    posix_time_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.654321+01:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

    expected_timestamp = -11644387200000000000
    posix_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)

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
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.987654321Z')

  def testGetDate(self):
    """Tests the GetDate function."""
    posix_time_object = posix_time.PosixTimeInNanoseconds(
        timestamp=1281643591987654321)

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    posix_time_object = posix_time.PosixTimeInNanoseconds()

    date_tuple = posix_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

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
