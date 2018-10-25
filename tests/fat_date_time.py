#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the FAT date time implementation."""

from __future__ import unicode_literals

import decimal
import unittest

from dfdatetime import fat_date_time


class FATDateTimeEpochTest(unittest.TestCase):
  """Tests for the FAT date time epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    fat_date_time_epoch = fat_date_time.FATDateTimeEpoch()
    self.assertIsNotNone(fat_date_time_epoch)


class FATDateTime(unittest.TestCase):
  """Tests for the FAT date time."""

  # pylint: disable=protected-access

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    fat_date_time_object = fat_date_time.FATDateTime(fat_date_time=0xa8d03d0c)

    normalized_timestamp = fat_date_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281647192.0'))

    fat_date_time_object = fat_date_time.FATDateTime()

    normalized_timestamp = fat_date_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    fat_date_time_object = fat_date_time.FATDateTime()

    expected_number_of_seconds = 966038400
    fat_date_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(
        fat_date_time_object._number_of_seconds, expected_number_of_seconds)

    expected_number_of_seconds = 966114391
    fat_date_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(
        fat_date_time_object._number_of_seconds, expected_number_of_seconds)

    expected_number_of_seconds = 966114391
    fat_date_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(
        fat_date_time_object._number_of_seconds, expected_number_of_seconds)

    expected_number_of_seconds = 966117991
    fat_date_time_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        fat_date_time_object._number_of_seconds, expected_number_of_seconds)

    expected_number_of_seconds = 966110791
    fat_date_time_object.CopyFromDateTimeString(
        '2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        fat_date_time_object._number_of_seconds, expected_number_of_seconds)

    expected_number_of_seconds = 86400
    fat_date_time_object.CopyFromDateTimeString('1980-01-02 00:00:00')
    self.assertEqual(
        fat_date_time_object._number_of_seconds, expected_number_of_seconds)

    with self.assertRaises(ValueError):
      fat_date_time_object.CopyFromDateTimeString('2200-01-02 00:00:00')

  def testGetNumberOfSeconds(self):
    """Tests the _GetNumberOfSeconds function."""
    fat_date_time_object = fat_date_time.FATDateTime()

    fat_date_time_object._GetNumberOfSeconds(0xa8d03d0c)

    # Invalid number of seconds.
    test_fat_date_time = (0xa8d03d0c & ~(0x1f << 16)) | ((30 & 0x1f) << 16)
    with self.assertRaises(ValueError):
      fat_date_time_object._GetNumberOfSeconds(test_fat_date_time)

    # Invalid number of minutes.
    test_fat_date_time = (0xa8d03d0c & ~(0x3f << 21)) | ((60 & 0x3f) << 21)
    with self.assertRaises(ValueError):
      fat_date_time_object._GetNumberOfSeconds(test_fat_date_time)

    # Invalid number of hours.
    test_fat_date_time = (0xa8d03d0c & ~(0x1f << 27)) | ((24 & 0x1f) << 27)
    with self.assertRaises(ValueError):
      fat_date_time_object._GetNumberOfSeconds(test_fat_date_time)

    # Invalid day of month.
    test_fat_date_time = (0xa8d03d0c & ~0x1f) | (32 & 0x1f)
    with self.assertRaises(ValueError):
      fat_date_time_object._GetNumberOfSeconds(test_fat_date_time)

    # Invalid month.
    test_fat_date_time = (0xa8d03d0c & ~(0x0f << 5)) | ((13 & 0x0f) << 5)
    with self.assertRaises(ValueError):
      fat_date_time_object._GetNumberOfSeconds(test_fat_date_time)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    fat_date_time_object = fat_date_time.FATDateTime(fat_date_time=0xa8d03d0c)

    date_time_string = fat_date_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 21:06:32')

    fat_date_time_object = fat_date_time.FATDateTime()

    date_time_string = fat_date_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    fat_date_time_object = fat_date_time.FATDateTime(fat_date_time=0xa8d03d0c)

    date_time_string = fat_date_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T21:06:32Z')

  def testGetDate(self):
    """Tests the GetDate function."""
    fat_date_time_object = fat_date_time.FATDateTime(fat_date_time=0xa8d03d0c)

    date_tuple = fat_date_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    fat_date_time_object = fat_date_time.FATDateTime()

    date_tuple = fat_date_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    fat_date_time_object = fat_date_time.FATDateTime(fat_date_time=0xa8d03d0c)

    time_of_day_tuple = fat_date_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (21, 6, 32))

    fat_date_time_object = fat_date_time.FATDateTime()

    time_of_day_tuple = fat_date_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
