#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the HFS time implementation."""

import decimal
import unittest

from dfdatetime import hfs_time


class HFSTimeEpochTest(unittest.TestCase):
  """Tests for the HFS time epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    hfs_time_epoch = hfs_time.HFSTimeEpoch()
    self.assertIsNotNone(hfs_time_epoch)


class HFSTimeTest(unittest.TestCase):
  """Tests for the HFS timestamp."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the properties."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)
    self.assertEqual(hfs_time_object.timestamp, 3458215528)

    hfs_time_object = hfs_time.HFSTime()
    self.assertIsNone(hfs_time_object.timestamp)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)

    normalized_timestamp = hfs_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1375370728.0'))

    hfs_time_object = hfs_time.HFSTime(
        time_zone_offset=60, timestamp=3458215528)

    normalized_timestamp = hfs_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1375367128.0'))

    hfs_time_object = hfs_time.HFSTime(timestamp=0x1ffffffff)

    normalized_timestamp = hfs_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

    hfs_time_object = hfs_time.HFSTime(timestamp=-0x1ffffffff)

    normalized_timestamp = hfs_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

    hfs_time_object = hfs_time.HFSTime()

    normalized_timestamp = hfs_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    hfs_time_object = hfs_time.HFSTime()

    hfs_time_object.CopyFromDateTimeString('2013-08-01')
    self.assertEqual(hfs_time_object._timestamp, 3458160000)
    self.assertEqual(hfs_time_object._time_zone_offset, 0)

    hfs_time_object.CopyFromDateTimeString('2013-08-01 15:25:28')
    self.assertEqual(hfs_time_object._timestamp, 3458215528)
    self.assertEqual(hfs_time_object._time_zone_offset, 0)

    hfs_time_object.CopyFromDateTimeString('2013-08-01 15:25:28.546875')
    self.assertEqual(hfs_time_object._timestamp, 3458215528)
    self.assertEqual(hfs_time_object._time_zone_offset, 0)

    hfs_time_object.CopyFromDateTimeString('2013-08-01 15:25:28.546875-01:00')
    self.assertEqual(hfs_time_object._timestamp, 3458215528)
    self.assertEqual(hfs_time_object._time_zone_offset, -60)

    hfs_time_object.CopyFromDateTimeString('2013-08-01 15:25:28.546875+01:00')
    self.assertEqual(hfs_time_object._timestamp, 3458215528)
    self.assertEqual(hfs_time_object._time_zone_offset, 60)

    hfs_time_object.CopyFromDateTimeString('1904-01-02 00:00:00')
    self.assertEqual(hfs_time_object._timestamp, 86400)
    self.assertEqual(hfs_time_object._time_zone_offset, 0)

    with self.assertRaises(ValueError):
      hfs_time_object.CopyFromDateTimeString('1600-01-02 00:00:00')

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)

    date_time_string = hfs_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2013-08-01 15:25:28')

    hfs_time_object = hfs_time.HFSTime()

    date_time_string = hfs_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)

    date_time_string = hfs_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2013-08-01T15:25:28+00:00')

  def testGetDate(self):
    """Tests the GetDate function."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)

    date_tuple = hfs_time_object.GetDate()
    self.assertEqual(date_tuple, (2013, 8, 1))

    hfs_time_object = hfs_time.HFSTime()

    date_tuple = hfs_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)

    date_with_time_of_day_tuple = hfs_time_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2013, 8, 1, 15, 25, 28))

    hfs_time_object = hfs_time.HFSTime()

    date_with_time_of_day_tuple = hfs_time_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)

    time_of_day_tuple = hfs_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (15, 25, 28))

    hfs_time_object = hfs_time.HFSTime()

    time_of_day_tuple = hfs_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
