#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the HFS time implementation."""

from __future__ import unicode_literals

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

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    hfs_time_object = hfs_time.HFSTime()

    expected_timestamp = 3458160000
    hfs_time_object.CopyFromDateTimeString('2013-08-01')
    self.assertEqual(hfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 3458215528
    hfs_time_object.CopyFromDateTimeString('2013-08-01 15:25:28')
    self.assertEqual(hfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 3458215528
    hfs_time_object.CopyFromDateTimeString('2013-08-01 15:25:28.546875')
    self.assertEqual(hfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 3458219128
    hfs_time_object.CopyFromDateTimeString('2013-08-01 15:25:28.546875-01:00')
    self.assertEqual(hfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 3458211928
    hfs_time_object.CopyFromDateTimeString('2013-08-01 15:25:28.546875+01:00')
    self.assertEqual(hfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 86400
    hfs_time_object.CopyFromDateTimeString('1904-01-02 00:00:00')
    self.assertEqual(hfs_time_object.timestamp, expected_timestamp)

    with self.assertRaises(ValueError):
      hfs_time_object.CopyFromDateTimeString('1600-01-02 00:00:00')

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)

    stat_time_tuple = hfs_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (1375370728, 0))

    hfs_time_object = hfs_time.HFSTime(timestamp=0x1ffffffff)

    stat_time_tuple = hfs_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

    hfs_time_object = hfs_time.HFSTime(timestamp=-0x1ffffffff)

    stat_time_tuple = hfs_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

    hfs_time_object = hfs_time.HFSTime()

    stat_time_tuple = hfs_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)

    date_time_string = hfs_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2013-08-01 15:25:28')

    hfs_time_object = hfs_time.HFSTime()

    date_time_string = hfs_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testGetDate(self):
    """Tests the GetDate function."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)

    date_tuple = hfs_time_object.GetDate()
    self.assertEqual(date_tuple, (2013, 8, 1))

    hfs_time_object._EPOCH.year = -1

    date_tuple = hfs_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

    hfs_time_object = hfs_time.HFSTime()

    date_tuple = hfs_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)

    micro_posix_timestamp = hfs_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, 1375370728000000)

    hfs_time_object = hfs_time.HFSTime(timestamp=0x1ffffffff)

    micro_posix_timestamp = hfs_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)

    hfs_time_object = hfs_time.HFSTime(timestamp=-0x1ffffffff)

    micro_posix_timestamp = hfs_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)

    hfs_time_object = hfs_time.HFSTime()

    micro_posix_timestamp = hfs_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
