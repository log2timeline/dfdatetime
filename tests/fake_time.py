#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the fake time implementation."""

import decimal
import unittest

from dfdatetime import fake_time


class FakeTimeTest(unittest.TestCase):
  """Tests for the fake time."""

  # pylint: disable=protected-access

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')

    normalized_timestamp = fake_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281647191.546875'))

    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875+01:00')

    normalized_timestamp = fake_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281643591.546875'))

    fake_time_object = fake_time.FakeTime()
    fake_time_object._number_of_seconds = None

    normalized_timestamp = fake_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    fake_time_object = fake_time.FakeTime()
    fake_time_object._normalized_timestamp = decimal.Decimal(
        '1333794697.6252465')
    plaso_timestamp = fake_time_object.GetPlasoTimestamp()
    self.assertEqual(plaso_timestamp, 1333794697625247)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    fake_time_object = fake_time.FakeTime()

    fake_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(fake_time_object._number_of_seconds, 1281571200)
    self.assertIsNone(fake_time_object._microseconds)
    self.assertEqual(fake_time_object._time_zone_offset, 0)

    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(fake_time_object._number_of_seconds, 1281647191)
    self.assertIsNone(fake_time_object._microseconds)
    self.assertEqual(fake_time_object._time_zone_offset, 0)

    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(fake_time_object._number_of_seconds, 1281647191)
    self.assertEqual(fake_time_object._microseconds, 546875)
    self.assertEqual(fake_time_object._time_zone_offset, 0)

    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(fake_time_object._number_of_seconds, 1281647191)
    self.assertEqual(fake_time_object._microseconds, 546875)
    self.assertEqual(fake_time_object._time_zone_offset, -60)

    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(fake_time_object._number_of_seconds, 1281647191)
    self.assertEqual(fake_time_object._microseconds, 546875)
    self.assertEqual(fake_time_object._time_zone_offset, 60)

    fake_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(fake_time_object._number_of_seconds, -11644387200)
    self.assertIsNone(fake_time_object._microseconds)
    self.assertEqual(fake_time_object._time_zone_offset, 0)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')

    date_time_string = fake_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 21:06:31.546875')

    fake_time_object = fake_time.FakeTime()
    fake_time_object._number_of_seconds = None

    date_time_string = fake_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')

    date_time_string = fake_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T21:06:31.546875+00:00')

  def testGetDate(self):
    """Tests the GetDate function."""
    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')

    date_tuple = fake_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    fake_time_object = fake_time.FakeTime()
    fake_time_object._number_of_seconds = None

    date_tuple = fake_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')

    date_with_time_of_day_tuple = fake_time_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2010, 8, 12, 21, 6, 31))

    fake_time_object = fake_time.FakeTime()
    fake_time_object._number_of_seconds = None

    date_with_time_of_day_tuple = fake_time_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')

    time_of_day_tuple = fake_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (21, 6, 31))

    fake_time_object = fake_time.FakeTime()
    fake_time_object._number_of_seconds = None

    time_of_day_tuple = fake_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
