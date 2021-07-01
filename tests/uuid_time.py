#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the UUID version 1 time implementation."""

import decimal
import uuid
import unittest

from dfdatetime import uuid_time


class UUIDTimeEpochTEst(unittest.TestCase):
  """Tests for the UUID version 1 time time epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    uuid_time_epoch = uuid_time.UUIDTimeEpoch()
    self.assertIsNotNone(uuid_time_epoch)


class UUIDTimeTest(unittest.TestCase):
  """Tests for the UUID version 1 timestamp."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the initialization function."""
    uuid_time_object = uuid_time.UUIDTime()
    self.assertIsNotNone(uuid_time_object)

    uuid_object = uuid.UUID('00911b54-9ef4-11e1-be53-525400123456')
    uuid_time_object = uuid_time.UUIDTime(timestamp=uuid_object.time)
    self.assertIsNotNone(uuid_time_object)
    expected_timestamp = 135564234616544084
    self.assertEqual(uuid_time_object.timestamp, expected_timestamp)

    with self.assertRaises(ValueError):
      uuid_time.UUIDTime(timestamp=0x1fffffffffffffff)

    with self.assertRaises(ValueError):
      uuid_time.UUIDTime(timestamp=-1)

  def testProperties(self):
    """Tests the properties."""
    uuid_object = uuid.UUID('00911b54-9ef4-11e1-be53-525400123456')
    uuid_time_object = uuid_time.UUIDTime(timestamp=uuid_object.time)
    self.assertEqual(uuid_time_object.timestamp, 0x1e19ef400911b54)

    uuid_time_object = uuid_time.UUIDTime()
    self.assertIsNone(uuid_time_object.timestamp)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    uuid_object = uuid.UUID('00911b54-9ef4-11e1-be53-525400123456')
    uuid_time_object = uuid_time.UUIDTime(timestamp=uuid_object.time)

    normalized_timestamp = uuid_time_object._GetNormalizedTimestamp()
    self.assertEqual(
        normalized_timestamp, decimal.Decimal('1337130661.6544084'))

    uuid_object = uuid.UUID('00911b54-9ef4-11e1-be53-525400123456')
    uuid_time_object = uuid_time.UUIDTime(
        time_zone_offset=60, timestamp=uuid_object.time)

    normalized_timestamp = uuid_time_object._GetNormalizedTimestamp()
    self.assertEqual(
        normalized_timestamp, decimal.Decimal('1337127061.6544084'))

    uuid_time_object = uuid_time.UUIDTime()
    uuid_time_object._timestamp = 0x1fffffffffffffff

    normalized_timestamp = uuid_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

    uuid_time_object = uuid_time.UUIDTime()
    uuid_time_object._timestamp = -1

    normalized_timestamp = uuid_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

    uuid_time_object = uuid_time.UUIDTime()

    normalized_timestamp = uuid_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    uuid_time_object = uuid_time.UUIDTime()

    uuid_time_object.CopyFromDateTimeString('2013-08-01')
    self.assertEqual(uuid_time_object._timestamp, 135946080000000000)
    self.assertEqual(uuid_time_object._time_zone_offset, 0)

    uuid_time_object.CopyFromDateTimeString('2013-08-01 15:25:28')
    self.assertEqual(uuid_time_object._timestamp, 135946635280000000)
    self.assertEqual(uuid_time_object._time_zone_offset, 0)

    uuid_time_object.CopyFromDateTimeString('2013-08-01 15:25:28.546875')
    self.assertEqual(uuid_time_object._timestamp, 135946635285468750)
    self.assertEqual(uuid_time_object._time_zone_offset, 0)

    uuid_time_object.CopyFromDateTimeString('2013-08-01 15:25:28.546875-01:00')
    self.assertEqual(uuid_time_object._timestamp, 135946635285468750)
    self.assertEqual(uuid_time_object._time_zone_offset, -60)

    uuid_time_object.CopyFromDateTimeString('2013-08-01 15:25:28.546875+01:00')
    self.assertEqual(uuid_time_object._timestamp, 135946635285468750)
    self.assertEqual(uuid_time_object._time_zone_offset, 60)

    uuid_time_object.CopyFromDateTimeString('1582-10-16 00:00:00')
    self.assertEqual(uuid_time_object._timestamp, 864000000000)
    self.assertEqual(uuid_time_object._time_zone_offset, 0)

    with self.assertRaises(ValueError):
      uuid_time_object.CopyFromDateTimeString('1570-01-02 00:00:00')

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    uuid_object = uuid.UUID('00911b54-9ef4-11e1-be53-525400123456')
    uuid_time_object = uuid_time.UUIDTime(timestamp=uuid_object.time)

    date_time_string = uuid_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2012-05-16 01:11:01.6544084')

    uuid_time_object = uuid_time.UUIDTime()

    date_time_string = uuid_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    uuid_object = uuid.UUID('00911b54-9ef4-11e1-be53-525400123456')
    uuid_time_object = uuid_time.UUIDTime(timestamp=uuid_object.time)

    date_time_string = uuid_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2012-05-16T01:11:01.6544084+00:00')

  def testGetDate(self):
    """Tests the GetDate function."""
    uuid_object = uuid.UUID('00911b54-9ef4-11e1-be53-525400123456')
    uuid_time_object = uuid_time.UUIDTime(timestamp=uuid_object.time)

    date_tuple = uuid_time_object.GetDate()
    self.assertEqual(date_tuple, (2012, 5, 16))

    uuid_time_object = uuid_time.UUIDTime()

    date_tuple = uuid_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    uuid_object = uuid.UUID('00911b54-9ef4-11e1-be53-525400123456')
    uuid_time_object = uuid_time.UUIDTime(timestamp=uuid_object.time)

    date_with_time_of_day_tuple = uuid_time_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2012, 5, 16, 1, 11, 1))

    uuid_time_object = uuid_time.UUIDTime()

    date_with_time_of_day_tuple = uuid_time_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    uuid_object = uuid.UUID('00911b54-9ef4-11e1-be53-525400123456')
    uuid_time_object = uuid_time.UUIDTime(timestamp=uuid_object.time)

    time_of_day_tuple = uuid_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (1, 11, 1))

    uuid_time_object = uuid_time.UUIDTime()

    time_of_day_tuple = uuid_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
