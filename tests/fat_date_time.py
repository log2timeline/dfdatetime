#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the FAT date time implementation."""

import unittest

from dfdatetime import fat_date_time


class FATDateTime(unittest.TestCase):
  """Tests for the FAT date time."""

  # pylint: disable=protected-access

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    fat_date_time_object = fat_date_time.FATDateTime()

    expected_number_of_seconds = 966038400
    fat_date_time_object.CopyFromString(u'2010-08-12')
    self.assertEqual(
        fat_date_time_object._number_of_seconds, expected_number_of_seconds)

    expected_number_of_seconds = 966114391
    fat_date_time_object.CopyFromString(u'2010-08-12 21:06:31')
    self.assertEqual(
        fat_date_time_object._number_of_seconds, expected_number_of_seconds)

    expected_number_of_seconds = 966114391
    fat_date_time_object.CopyFromString(u'2010-08-12 21:06:31.546875')
    self.assertEqual(
        fat_date_time_object._number_of_seconds, expected_number_of_seconds)

    expected_number_of_seconds = 966117991
    fat_date_time_object.CopyFromString(u'2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        fat_date_time_object._number_of_seconds, expected_number_of_seconds)

    expected_number_of_seconds = 966110791
    fat_date_time_object.CopyFromString(u'2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        fat_date_time_object._number_of_seconds, expected_number_of_seconds)

    expected_number_of_seconds = 86400
    fat_date_time_object.CopyFromString(u'1980-01-02 00:00:00')
    self.assertEqual(
        fat_date_time_object._number_of_seconds, expected_number_of_seconds)

    with self.assertRaises(ValueError):
      fat_date_time_object.CopyFromString(u'2200-01-02 00:00:00')

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

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    fat_date_time_object = fat_date_time.FATDateTime(fat_date_time=0xa8d03d0c)

    expected_stat_time_tuple = (1281647192, None)
    stat_time_tuple = fat_date_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    fat_date_time_object = fat_date_time.FATDateTime()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = fat_date_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    fat_date_time_object = fat_date_time.FATDateTime(fat_date_time=0xa8d03d0c)

    expected_micro_posix_timestamp = 1281647192000000
    micro_posix_timestamp = fat_date_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

    fat_date_time_object = fat_date_time.FATDateTime()

    micro_posix_timestamp = fat_date_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
