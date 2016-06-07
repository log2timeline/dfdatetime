#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the FAT date time implementation."""

import unittest

from dfdatetime import fat_date_time


class FATDateTime(unittest.TestCase):
  """Tests for the FAT date time object."""

  def testGetNumberOfSeconds(self):
    """Tests the GetNumberOfSeconds function."""
    fat_date_time.FATDateTime(0xa8d03d0c)

    # Invalid number of seconds.
    with self.assertRaises(ValueError):
      fat_date_time.FATDateTime(
          (0xa8d03d0c & ~(0x1f << 16)) | ((30 & 0x1f) << 16))

    # Invalid number of minutes.
    with self.assertRaises(ValueError):
      fat_date_time.FATDateTime(
          (0xa8d03d0c & ~(0x3f << 21)) | ((60 & 0x3f) << 21))

    # Invalid number of hours.
    with self.assertRaises(ValueError):
      fat_date_time.FATDateTime(
          (0xa8d03d0c & ~(0x1f << 27)) | ((24 & 0x1f) << 27))

    # Invalid day of month.
    with self.assertRaises(ValueError):
      fat_date_time.FATDateTime((0xa8d03d0c & ~0x1f) | (32 & 0x1f))

    # Invalid month.
    with self.assertRaises(ValueError):
      fat_date_time.FATDateTime(
          (0xa8d03d0c & ~(0x0f << 5)) | ((13 & 0x0f) << 5))

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    fat_date_time_object = fat_date_time.FATDateTime(0xa8d03d0c)

    expected_stat_time_tuple = (1281733592, 0)
    stat_time_tuple = fat_date_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    fat_date_time_object = fat_date_time.FATDateTime(0xa8d03d0c)

    expected_micro_posix_timestamp = 1281733592000000
    micro_posix_timestamp = fat_date_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
